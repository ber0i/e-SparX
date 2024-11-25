"""
Large part of this script is taken from
https://github.com/pytorch/tutorials/blob/main/beginner_source/hyperparameter_tuning_tutorial.py
"""

import argparse
import json
import os
import sys
import tempfile
from functools import partial
from pathlib import Path

import esparx
import ray.cloudpickle as pickle
import torch
from ray import train, tune
from ray.train import Checkpoint, get_checkpoint
from ray.tune.schedulers import ASHAScheduler
from torch.utils.data import DataLoader, Subset

project_base_path = os.getcwd()
sys.path.append(os.path.join(project_base_path, "usecases/wpf/bob"))
os.environ["PYTHONPATH"] = os.path.join(project_base_path, "usecases/wpf/bob")

from esparx_artifacts import PenmanshielDataset  # noqa: E402
from esparx_artifacts import LSTM, MLP  # noqa: E402


def train_model(config, args):

    args.batch_size = config["batch_size"]
    args.learning_rate = config["learning_rate"]
    args.n_hidden_neurons = config["n_hidden_neurons"]
    args.n_hidden_layers = config["n_hidden_layers"]
    args.dropout_rate = config["dropout_rate"]

    model_dict = {
        "mlp": MLP,
        "lstm": LSTM,
    }
    model = model_dict[args.model](args)

    model.to(args.device)

    loss_fn = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)

    checkpoint = get_checkpoint()
    if checkpoint:
        with checkpoint.as_directory() as checkpoint_dir:
            data_path = Path(checkpoint_dir) / "data.pkl"
            with open(data_path, "rb") as fp:
                checkpoint_state = pickle.load(fp)
            start_epoch = checkpoint_state["epoch"]
            model.load_state_dict(checkpoint_state["net_state_dict"])
            optimizer.load_state_dict(checkpoint_state["optimizer_state_dict"])
    else:
        start_epoch = 0

    dataset = PenmanshielDataset(
        data_file=os.path.join(project_base_path, args.data_path),
        lookback_timesteps=args.lookback_timesteps,
        forecast_timesteps=args.forecast_timesteps,
    )

    n = len(dataset)
    n_train = int(args.train_share * n)  # 70% for training
    n_val = int(args.val_share * n)  # 15% for validation

    dataset_train = Subset(dataset, range(0, n_train))
    dataset_val = Subset(dataset, range(n_train, n_train + n_val))

    loader_train = DataLoader(dataset_train, batch_size=args.batch_size)
    loader_val = DataLoader(dataset_val, batch_size=args.batch_size)

    for epoch in range(start_epoch, 10):  # loop over the dataset multiple times
        model.train()
        running_loss = 0.0
        epoch_steps = 0
        for batch, (X, y) in enumerate(loader_train):

            X = X.to(device=args.device)
            y = y.to(device=args.device)
            optimizer.zero_grad()
            y_pred = model(X)
            loss = loss_fn(y_pred, y)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.cpu().item()
            epoch_steps += 1

            # show loss every 100 steps
            if batch % 100 == 0:
                print(
                    f"Epoch {epoch}, batch {batch}, train MSE: {running_loss/epoch_steps:.4f}"
                )

        model.eval()
        # Validation loss
        val_loss = 0.0
        val_steps = 0
        for batch, (X, y) in enumerate(loader_val):

            X = X.to(device=args.device)
            y = y.to(device=args.device)
            y_pred = model(X)
            loss = loss_fn(y_pred, y)
            val_loss += loss.cpu().item()
            val_steps += 1

        checkpoint_data = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
        }

        with tempfile.TemporaryDirectory() as checkpoint_dir:
            data_path = Path(checkpoint_dir) / "data.pkl"
            with open(data_path, "wb") as fp:
                pickle.dump(checkpoint_data, fp)

            checkpoint = Checkpoint.from_directory(checkpoint_dir)
            train.report(
                {"loss": val_loss / val_steps},
                checkpoint=checkpoint,
            )

    print("Finished Training")


def main():

    parser = argparse.ArgumentParser(
        description="Wind Power Forecasting - MLP and LSTM Hyperparameter Tuning"
    )
    parser.add_argument(
        "--demo",
        type=bool,
        default=False,
        help="Run the script in demo mode. Default: False.",
    )
    parser.add_argument(
        "--num_samples",
        type=int,
        default=10,
        help="Number of samples to run hyperparameter tuning",
    )
    parser.add_argument(
        "--max_num_epochs",
        type=int,
        default=10,
        help="Maximum number of epochs to train the model",
    )
    parser.add_argument(
        "--hp_file",
        type=str,
        default="usecases/wpf/bob/esparx_artifacts/hyperparameters/mlp.json",
        help="Path to hyperparameters file. Default: usecases/wpf/bob/esparx_artifacts/hyperparameters/mlp.json.",
    )
    parser.add_argument(
        "--data_path",
        type=str,
        default="usecases/wpf/bob/esparx_artifacts/datasets/Cleaned_Data.csv",
        help="Path to data file. Default: usecases/wpf/bob/esparx_artifacts/datasets/Cleaned_Data.csv",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="mlp",
        help="Model to tune hyperparameters for. Options: mlp, lstm. Default: mlp.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device to run the model on. Options: cpu, cuda. Default: cpu.",
    )
    args = parser.parse_args()

    model_name = "MLP" if args.model == "mlp" else "LSTM"

    print(">>>>>>>>>>Registering this script in e-SparX<<<<<<<<<<")
    esparx.register_code(
        name="MLP/LSTM Hyperparameter Tuning",
        description="Script for tuning hyperparameters for MLP and LSTM models for wind power forecasting.",
        file_type="PY",
        source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/src/a_hp_tuning.py",
        download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/src/a_hp_tuning.py?inline=false",
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="Cleaned Data",
    )
    esparx.connect(
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="Penmanshiel Torch Dataset Class",
        target_name="MLP/LSTM Hyperparameter Tuning",
    )
    esparx.connect(
        pipeline_name="Wind Power Forecasting - TFT",
        source_name=f"{model_name}",
        target_name="MLP/LSTM Hyperparameter Tuning",
    )

    hp_file = os.path.join(project_base_path, args.hp_file)

    with open(hp_file, "r") as f:
        hp = json.load(f)

    for key, value in hp.items():
        setattr(args, key, value)

    config = {
        "batch_size": tune.choice([8, 16, 32, 64, 128]),
        "learning_rate": tune.loguniform(1e-4, 1e-1),
        "n_hidden_neurons": tune.choice([2**i for i in range(2, 9)]),
        "n_hidden_layers": tune.choice([1, 2, 3, 4]),
        "dropout_rate": tune.uniform(0.0, 0.5),
    }

    scheduler = ASHAScheduler(
        metric="loss",
        mode="min",
        max_t=args.max_num_epochs,
        grace_period=1,
        reduction_factor=2,
    )

    def custom_trial_dirname(Trial):
        # Use a shorter naming scheme for trials
        return f"trial_{Trial.trial_id}"

    if not args.demo:

        result = tune.run(
            partial(train_model, args=args),
            resources_per_trial={"cpu": 2, "gpu": 0},
            config=config,
            num_samples=args.num_samples,
            scheduler=scheduler,
            storage_path=os.path.join(
                project_base_path, "usecases", "wpf", "bob", "hp_tuning_results"
            ),
            trial_dirname_creator=custom_trial_dirname,
        )

        best_trial = result.get_best_trial("loss", "min", "last")
        print(f"Best trial config: {best_trial.config}")
        print(f"Best trial final validation loss: {best_trial.last_result['loss']}")

        hyperparameters_tuned = {
            "lookback_timesteps": args.lookback_timesteps,
            "forecast_timesteps": args.forecast_timesteps,
            "batch_size": best_trial.config["batch_size"],
            "n_epochs": args.n_epochs,
            "train_share": args.train_share,
            "val_share": args.val_share,
            "test_share": args.test_share,
            "learning_rate": best_trial.config["learning_rate"],
            "train_loss_fn": args.train_loss_fn,
            "n_hidden_neurons": best_trial.config["n_hidden_neurons"],
            "n_hidden_layers": best_trial.config["n_hidden_layers"],
            "dropout_rate": best_trial.config["dropout_rate"],
            "norm_layer": args.norm_layer,
            "activation": args.activation,
            "optimizer": args.optimizer,
        }
        with open(
            f"usecases/wpf/bob/hyperparameters/{args.model}_tuned.json", "w"
        ) as json_file:
            json.dump(hyperparameters_tuned, json_file)

    else:

        if args.model == "mlp":
            hyperparameters_tuned = {
                "lookback_timesteps": 12,
                "forecast_timesteps": 6,
                "batch_size": 16,
                "n_epochs": 50,
                "train_share": 0.7,
                "val_share": 0.15,
                "test_share": 0.15,
                "learning_rate": 0.00014240453648080826,
                "train_loss_fn": "mse",
                "n_hidden_neurons": 128,
                "n_hidden_layers": 3,
                "dropout_rate": 0.4024146368395615,
                "norm_layer": "layer",
                "activation": "relu",
                "optimizer": "adam",
            }
        elif args.model == "lstm":
            hyperparameters_tuned = {
                "lookback_timesteps": 12,
                "forecast_timesteps": 6,
                "batch_size": 16,
                "n_epochs": 50,
                "train_share": 0.7,
                "val_share": 0.15,
                "test_share": 0.15,
                "learning_rate": 0.0003336158404817423,
                "train_loss_fn": "mse",
                "n_hidden_neurons": 32,
                "n_hidden_layers": 4,
                "dropout_rate": 0.4829036456853215,
                "norm_layer": "layer",
                "activation": "relu",
                "optimizer": "adam",
            }

    print(">>>>>>>>>>Registering tuned hyperparameters in e-SparX<<<<<<<<<<")
    esparx.register_hyperparameters(
        name=f"{model_name} Tuned Hyperparameters",
        description=f"Hyperparameters for {model_name} after running a hyperparameter tuning.",
        hyperparameters=hyperparameters_tuned,
        file_type="JSON",
        source_url=f"https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/hyperparameters/{args.model}_tuned.py",
        download_url=f"https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/hyperparameters/{args.model}_tuned.py?inline=false",  # noqa: E501
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="MLP/LSTM Hyperparameter Tuning",
    )


if __name__ == "__main__":
    main()
