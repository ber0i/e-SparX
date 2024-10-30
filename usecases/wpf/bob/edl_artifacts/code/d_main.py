import argparse
import json
import os

import energydatalab as edl
import lstm
import mlp
import numpy as np
import torch
import wandb
from penmanshiel import PenmanshielDataset
from torch.utils.data import DataLoader, Subset


def main():

    print(">>>>>>>>>>Registering this script in EDL<<<<<<<<<<")
    edl.register_code(
        name="Main",
        description="Script to train and evaluate a model for wind power forecasting.",
        file_type="PY",
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="Cleaned Data",
    )

    parser = argparse.ArgumentParser(
        description="Wind Power Forecasting - MLP and LSTM"
    )
    parser.add_argument(
        "--demo",
        type=bool,
        default=False,
        help="Run the script in demo mode (no training, just registering). Default: False.",
    )
    parser.add_argument(
        "--hp_file",
        type=str,
        default="usecases/wpf/bob/hyperparameters/mlp_tuned.json",
        help="Path to hyperparameters file. Default: usecases/wpf/bob/hyperparameters/mlp_tuned.json.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="mlp",
        help="Model architecture to use. Options: mlp, lstm. Default: mlp.",
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device to use for training. Options: cpu, cuda. Default: cpu.",
    )
    parser.add_argument(
        "--wandb",
        type=bool,
        default=False,
        help="Use Weights and Biases for logging. Default: False.",
    )
    parser.add_argument(
        "--wandb_project_name",
        type=str,
        default="Wind Power Forecasting - MLP and LSTM",
        help="Weights and Biases project name. Default: Wind Power Forecasting.",
    )
    args = parser.parse_args()

    # Load and extract hyperparameters

    with open(args.hp_file, "r") as f:
        hp = json.load(f)

    for key, value in hp.items():
        setattr(args, key, value)

    # Register hyperparameters

    model_name_dict = {
        "mlp": "MLP",
        "lstm": "LSTM",
    }
    model_name = model_name_dict[args.model]

    # Data Preparation

    dataset = PenmanshielDataset(
        data_file="usecases/wpf/bob/edl_artifacts/datasets/Cleaned_Data.csv",
        lookback_timesteps=args.lookback_timesteps,
        forecast_timesteps=args.forecast_timesteps,
    )

    n = len(dataset)
    n_train = int(args.train_share * n)  # 70% for training
    n_val = int(args.val_share * n)  # 15% for validation
    n_test = n - n_train - n_val  # Remaining 15% for testing

    dataset_train = Subset(dataset, range(0, n_train))
    dataset_val = Subset(dataset, range(n_train, n_train + n_val))
    dataset_test = Subset(dataset, range(n_train + n_val, n_train + n_val + n_test))

    loader_train = DataLoader(dataset_train, batch_size=args.batch_size)
    loader_val = DataLoader(dataset_val, batch_size=args.batch_size)
    loader_test = DataLoader(dataset_test, batch_size=args.batch_size)

    # Model Preparation

    model_dict = {
        "mlp": mlp,
        "lstm": lstm,
    }
    model = model_dict[args.model].Model(args)

    model.to(device=args.device)

    if args.optimizer == "adam":
        optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)
    else:
        raise ValueError(f"Unknown optimizer {args.optimizer}")

    if args.wandb:
        wandb.init(
            project=args.wandb_project_name,
            name=f"{args.model}_{args.lookback_timesteps}_{args.forecast_timesteps}_{args.n_epochs}",
            dir=os.path.join(os.getcwd(), "usecases", "wpf", "bob", "wandb"),
        )

    # set training loss function
    if args.train_loss_fn == "mse":
        loss_fn = torch.nn.MSELoss()
    else:
        raise ValueError(f"Unknown loss function {args.train_loss_fn}")

    if not args.demo:

        # Training

        print("Training starts.")

        for epoch in range(args.n_epochs):
            model.train()
            loss_list = []
            for batch, (X, y) in enumerate(loader_train):
                X = X.to(device=args.device)
                y = y.to(device=args.device)
                optimizer.zero_grad()
                y_pred = model(X)
                loss = loss_fn(y_pred, y)
                loss.backward()
                optimizer.step()
                loss_list.append(loss.cpu().item())

                # show loss every 100 steps
                if batch % 100 == 0:
                    print(
                        f"Epoch {epoch}, batch {batch}, train MSE: {sum(loss_list)/len(loss_list):.4f}"
                    )

            print(f"Epoch {epoch}, train MSE: {sum(loss_list)/len(loss_list):.4f}")
            if args.wandb:
                wandb.log({"train_mse": sum(loss_list) / len(loss_list)})

            model.eval()
            loss_list = []
            for batch, (X, y) in enumerate(loader_val):
                X = X.to(device=args.device)
                y = y.to(device=args.device)
                y_pred = model(X)
                loss = loss_fn(y_pred, y)
                loss_list.append(loss.cpu().item())

            print(f"Epoch {epoch}, val MSE: {sum(loss_list)/len(loss_list):.4f}")
            if args.wandb:
                wandb.log({"val_mse": sum(loss_list) / len(loss_list)})

        # Testing

        print("Training finished, evaluating on test set starts.")

        model.eval()
        loss_list = []
        for batch, (X, y) in enumerate(loader_test):
            X = X.to(device=args.device)
            y = y.to(device=args.device)
            y_pred = model(X)
            loss = loss_fn(y_pred, y)
            loss_list.append(loss.cpu().item())

        print(f"Test MSE: {sum(loss_list)/len(loss_list):.4f}")
        print(f"Test RMSE: {np.sqrt(sum(loss_list)/len(loss_list)):.4f}")

        if args.wandb:
            wandb.log({"test_mse": sum(loss_list) / len(loss_list)})
            wandb.log({"test_rmse": np.sqrt(sum(loss_list) / len(loss_list))})
            wandb.finish()

        print(">>>>>>>>>>Registering results in EDL<<<<<<<<<<")
        edl.register_results(
            name=f"{model_name} Results Tuned",
            description=f"Error metric values of the {model_name} model on the test dataset after hyperparameter tuning.",
            results={
                "MSE": sum(loss_list) / len(loss_list),
                "RMSE": np.sqrt(sum(loss_list) / len(loss_list)),
            },
            pipeline_name="Wind Power Forecasting - TFT",
            source_name="Main",
        )

    else:

        print("Demo mode, no training performed. Registering mock results")
        # These are the results when training with seed = 42.
        if args.model == "mlp":
            mock_results = {
                "MSE": 0.014492,
                "RMSE": 0.12038,
            }
        elif args.model == "lstm":
            mock_results = {
                "MSE": 0.0136,
                "RMSE": 0.11662,
            }
        edl.register_results(
            name=f"{model_name} Results Tuned",
            description=f"Error metric values of the {model_name} model on the test dataset after hyperparameter tuning.",
            results=mock_results,
            pipeline_name="Wind Power Forecasting - TFT",
            source_name="Main",
        )

    print(">>>>>>>>>>Setting additional pipeline connections in EDL<<<<<<<<<<")
    edl.connect(
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="Penmanshiel Torch Dataset Class",
        target_name="Main",
    )
    edl.connect(
        pipeline_name="Wind Power Forecasting - TFT",
        source_name=f"{model_name}",
        target_name="Main",
    )
    edl.connect(
        pipeline_name="Wind Power Forecasting - TFT",
        source_name=f"{model_name} Tuned Hyperparameters",
        target_name="Main",
    )
    edl.connect(
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="Main",
        target_name="Persistence Results",
    )

    # Save model parameters

    if not args.demo:
        torch.save(
            model.state_dict(),
            f"usecases/wpf/bob/models/{model_name}_tuned.pth",
        )
        print("Model parameters saved.")

    print(">>>>>>>>>>Registering parameters in EDL<<<<<<<<<<")
    edl.register_parameters(
        name=f"{model_name} Parameters Tuned",
        description=f"Trained parameters of the {model_name} model with tuned hyperparameters.",
        file_type="PTH",
        source_url=f"https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/models/{model_name}_tuned.pth",
        download_url=f"https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/bob/models/{model_name}_tuned.pth?inline=false",  # noqa: E501
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="Main",
    )


if __name__ == "__main__":
    main()
