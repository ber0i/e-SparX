import argparse
import json
import os

import energydatalab as edl
import numpy as np
import torch
import wandb
from datasets import PenmanshielDataset
from models import lstm, mlp
from torch.utils.data import DataLoader, Subset


def main():

    print(">>>>>>>>>>Registering this script in EDL<<<<<<<<<<")
    edl.register_code(
        name="Main",
        description="Script to train and evaluate a model for wind power forecasting.",
        file_type="PY",
        source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/src/d_main.py",
        download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/src/d_main.py?inline=false",
        pipeline_name="Wind Power Forecasting - MLP and LSTM",
        parent_name="Cleaned Data",
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
        default="usecases/wpf/alice/hyperparameters/mlp.json",
        help="Path to hyperparameters file. Default: usecases/wpf/alice/hyperparameters/mlp.json.",
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
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed. Default: 42.",
    )
    args = parser.parse_args()

    # Set random seed for reproducibility
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

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

    print(">>>>>>>>>>Registering hyperparameters in EDL<<<<<<<<<<")
    edl.register_hyperparameters(
        name=f"{model_name} Hyperparameters",
        description=f"Hyperparameters for the {model_name} model.",
        hyperparameters=hp,
        file_type="JSON",
        source_url=f"https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/hyperparameters/{args.model}.json",
        download_url=f"https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/hyperparameters/{args.model}.json?inline=false",  # noqa: E501
        pipeline_name="Wind Power Forecasting - MLP and LSTM",
    )

    # Data Preparation

    dataset = PenmanshielDataset(
        data_file="usecases/wpf/alice/data/cleaned/Cleaned_Data.csv",
        lookback_timesteps=args.lookback_timesteps,
        forecast_timesteps=args.forecast_timesteps,
    )

    print(">>>>>>>>>>Registering the dataset class code in EDL<<<<<<<<<<")
    edl.register_code(
        name="Penmanshiel Torch Dataset Class",
        description="Code defining the PyTorch dataset class for the Penmanshiel dataset.",
        file_type="PY",
        source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/src/datasets/penmanshiel.py",
        download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/src/datasets/penmanshiel.py?inline=false",
        pipeline_name="Wind Power Forecasting - MLP and LSTM",
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

    print(">>>>>>>>>>Registering model in EDL<<<<<<<<<<")
    edl.register_model_pytorch(
        name=f"{model_name}",
        description=f"PyTorch nn.Module class for a {model_name} wind power forecasting model.",
        file_type="PY",
        model=model,
        input_example=next(iter(loader_train))[0],
        source_url=f"https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/src/models/{args.model}.py",
        download_url=f"https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/src/models/{args.model}.py?inline=false",
        pipeline_name="Wind Power Forecasting - MLP and LSTM",
    )

    model.to(device=args.device)

    if args.optimizer == "adam":
        optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)
    else:
        raise ValueError(f"Unknown optimizer {args.optimizer}")

    if args.wandb:
        wandb.init(
            project=args.wandb_project_name,
            name=f"{args.model}_{args.lookback_timesteps}_{args.forecast_timesteps}_{args.n_epochs}",
            dir=os.path.join(os.getcwd(), "usecases", "wpf", "alice", "wandb"),
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
        loss_list_persistence = []
        for batch, (X, y) in enumerate(loader_test):
            X = X.to(device=args.device)
            y = y.to(device=args.device)
            y_pred = model(X)
            loss = loss_fn(y_pred, y)
            loss_list.append(loss.cpu().item())

            # persistence prediction
            last_power = X[:, args.lookback_timesteps - 1]
            y_pred_persistence = last_power.unsqueeze(1).expand(
                -1, hp["forecast_timesteps"]
            )
            loss_persistence = loss_fn(y_pred_persistence, y)
            loss_list_persistence.append(loss_persistence.cpu().item())

        print(f"Test MSE: {sum(loss_list)/len(loss_list):.4f}")
        print(f"Test RMSE: {np.sqrt(sum(loss_list)/len(loss_list)):.4f}")

        print(
            f"Test MSE Persistence: {sum(loss_list_persistence)/len(loss_list_persistence):.4f}"
        )
        print(
            f"Test RMSE Persistence: {np.sqrt(sum(loss_list_persistence)/len(loss_list_persistence)):.4f}"
        )

        if args.wandb:
            wandb.log({"test_mse": sum(loss_list) / len(loss_list)})
            wandb.log({"test_rmse": np.sqrt(sum(loss_list) / len(loss_list))})
            wandb.finish()

        print(">>>>>>>>>>Registering results in EDL<<<<<<<<<<")
        edl.register_results(
            name=f"{model_name} Results",
            description=f"Error metric values of the {model_name} model on the test dataset.",
            results={
                "MSE": sum(loss_list) / len(loss_list),
                "RMSE": np.sqrt(sum(loss_list) / len(loss_list)),
            },
            pipeline_name="Wind Power Forecasting - MLP and LSTM",
            parent_name="Main",
        )
        edl.register_results(
            name="Persistence Results",
            description="Error metric values of the persistence model on the test dataset.",
            results={
                "MSE": sum(loss_list_persistence) / len(loss_list_persistence),
                "RMSE": np.sqrt(
                    sum(loss_list_persistence) / len(loss_list_persistence)
                ),
            },
            pipeline_name="Wind Power Forecasting - MLP and LSTM",
            parent_name="Main",
        )

    else:
        print("Demo mode, no training performed. Registering mock results")
        # Info: The mock results are the results obtained when running the script with seed = 42.
        if args.model == "mlp":
            mock_results = {
                "MSE": 0.01642,
                "RMSE": 0.12814,
            }
        elif args.model == "lstm":
            mock_results = {
                "MSE": 0.014245,
                "RMSE": 0.11935,
            }
        mock_results_persistence = {
            "MSE": 0.1275,
            "RMSE": 0.3571,
        }
        edl.register_results(
            name=f"{model_name} Results",
            description=f"Error metric values of the {model_name} model on the test dataset.",
            results=mock_results,
            pipeline_name="Wind Power Forecasting - MLP and LSTM",
            parent_name="Main",
        )
        edl.register_results(
            name="Persistence Results",
            description="Error metric values of the persistence model on the test dataset.",
            results=mock_results_persistence,
            pipeline_name="Wind Power Forecasting - MLP and LSTM",
            parent_name="Main",
        )

    print(">>>>>>>>>>Setting additional pipeline connections in EDL<<<<<<<<<<")
    edl.connect(
        pipeline_name="Wind Power Forecasting - MLP and LSTM",
        parent_name="Penmanshiel Torch Dataset Class",
        target_name="Main",
    )
    edl.connect(
        pipeline_name="Wind Power Forecasting - MLP and LSTM",
        parent_name=f"{model_name}",
        target_name="Main",
    )
    edl.connect(
        pipeline_name="Wind Power Forecasting - MLP and LSTM",
        parent_name=f"{model_name} Hyperparameters",
        target_name="Main",
    )

    # Save model parameters

    if not args.demo:
        torch.save(
            model.state_dict(),
            f"usecases/wpf/alice/models/{model_name}.pth",
        )
        print("Model parameters saved.")

    print(">>>>>>>>>>Registering parameters in EDL<<<<<<<<<<")
    edl.register_parameters(
        name=f"{model_name} Parameters",
        description=f"Trained parameters of the {model_name} model.",
        file_type="PTH",
        source_url=f"https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/models/{model_name}.pth",
        download_url=f"https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/models/{model_name}.pth?inline=false",  # noqa: E501
        pipeline_name="Wind Power Forecasting - MLP and LSTM",
        parent_name="Main",
    )


if __name__ == "__main__":
    main()
