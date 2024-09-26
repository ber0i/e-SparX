import argparse

import energy_data_lab as edl
import torch
import wandb
from data.datasets import PenmanshielDataset
from models import mlp
from torch.utils.data import DataLoader, Subset


def main():

    parser = argparse.ArgumentParser(description="Wind Power Forecasting")
    parser.add_argument(
        "--lookback_timesteps",
        type=int,
        default=12,
        help="Number of lookback timesteps. Default: 12.",
    )
    parser.add_argument(
        "--forecast_timesteps",
        type=int,
        default=6,
        help="Number of forecast timesteps. Default: 6.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=64,
        help="Number of time windows per batch. Default: 64.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="mlp",
        help="Model architecture to use. Options: mlp. Default: mlp.",
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
        default="Wind Power Forecasting",
        help="Weights and Biases project name. Default: Wind Power Forecasting.",
    )
    parser.add_argument(
        "--n_epochs",
        type=int,
        default=1,
        help="Number of epochs to train the model. Default: 1.",
    )
    parser.add_argument(
        "--train_share",
        type=float,
        default=0.7,
        help="Fraction of data to use for training. Default: 0.7.",
    )
    parser.add_argument(
        "--val_share",
        type=float,
        default=0.15,
        help="Fraction of data to use for validation. Default: 0.15.",
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=1e-3,
        help="Learning rate for training. Default: 1e-3.",
    )
    parser.add_argument(
        "--train_loss_fn",
        type=str,
        default="MSE",
        help="Loss function to use for training. Options: MSE. Default: MSE.",
    )
    parser.add_argument(
        "--n_hidden_neurons",
        type=int,
        default=512,
        help="Number of hidden neurons. Default: 512.",
    )
    parser.add_argument(
        "--n_hidden_layers",
        type=int,
        default=2,
        help="Number of hidden layers. Default: 2.",
    )
    parser.add_argument(
        "--dropout_rate",
        type=float,
        default=0.05,
        help="Dropout rate. Default: 0.05.",
    )
    parser.add_argument(
        "--norm_layer",
        type=str,
        default="layer",
        help="Normalization layer. Options: layer, batch. Default: layer.",
    )
    parser.add_argument(
        "--activation",
        type=str,
        default="relu",
        help="Activation function. Options: relu, leaky_relu. Default: relu.",
    )
    args = parser.parse_args()

    # Data Preparation

    dataset = PenmanshielDataset(
        data_file="usecases/wpf/data/cleaned/Cleaned_Data.csv",
        lookback_timesteps=args.lookback_timesteps,
        forecast_timesteps=args.forecast_timesteps,
    )

    edl.register_code(
        name="Penmanshiel Torch Dataset Class",
        description="Code defining the PyTorch dataset class for the Penmanshiel dataset.",
        file_type="PY",
        source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/src/data/datasets/penmanshiel.py",
        download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/src/data/datasets/penmanshiel.py?inline=false",
        pipeline_name="Wind Power Forecasting",
    )

    n = len(dataset)
    # TODO: REMOVE THIS LINE (FOR DEBUGGING PURPOSES ONLY)
    n = 1000
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
    }
    model = model_dict[args.model].Model(args)
    model.to(device=args.device)

    if args.model == "mlp":
        edl.register_model_pytorch(
            name="MLP",
            description="PyTorch nn.Module class for the Multilayer Perceptron (MLP) model.",
            file_type="PY",
            model=model,
            input_example=next(iter(loader_train))[0],
            source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/src/models/mlp.py",
            download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/src/models/mlp.py?inline=false",
            pipeline_name="Wind Power Forecasting",
        )

    hyperparameters = [
        {"name": "lookback_timesteps", "value": args.lookback_timesteps},
        {"name": "forecast_timesteps", "value": args.forecast_timesteps},
        {"name": "batch_size", "value": args.batch_size},
        {"name": "n_epochs", "value": args.n_epochs},
        {"name": "train_share", "value": args.train_share},
        {"name": "val_share", "value": args.val_share},
        {
            "name": "test_share",
            "value": round(1 - args.train_share - args.val_share, 2),
        },
        {"name": "learning_rate", "value": args.learning_rate},
        {"name": "train_loss_fn", "value": args.train_loss_fn},
        {"name": "n_hidden_neurons", "value": args.n_hidden_neurons},
        {"name": "n_hidden_layers", "value": args.n_hidden_layers},
        {"name": "dropout_rate", "value": args.dropout_rate},
        {"name": "norm_layer", "value": args.norm_layer},
        {"name": "activation", "value": args.activation},
    ]

    if args.model == "mlp":
        edl.register_hyperparameters(
            name="MLP Hyperparameters",
            description="Hyperparameters for the MLP model.",
            hyperparameters=hyperparameters,
            pipeline_name="Wind Power Forecasting",
        )

    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)

    if args.wandb:
        wandb.init(
            project=args.wandb_project_name,
            name=f"{args.model}_{args.lookback_timesteps}_{args.forecast_timesteps}",
        )

    # set training loss function
    if args.train_loss_fn == "MSE":
        loss_fn = torch.nn.MSELoss()
    else:
        raise ValueError(f"Unknown loss function {args.train_loss_fn}")

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

    # Compute test loss
    model.eval()
    loss_list = []
    for batch, (X, y) in enumerate(loader_test):
        X = X.to(device=args.device)
        y = y.to(device=args.device)
        y_pred = model(X)
        loss = loss_fn(y_pred, y)
        loss_list.append(loss.cpu().item())

    print(f"Test MSE: {sum(loss_list)/len(loss_list):.4f}")
    if args.wandb:
        wandb.log({"test_mse": sum(loss_list) / len(loss_list)})
        wandb.finish()

    edl.register_code(
        name="Main",
        description="Script to train and evaluate a model for wind power forecasting.",
        file_type="PY",
        source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/src/main.py",
        download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/src/main.py?inline=false",
        pipeline_name="Wind Power Forecasting",
        parent_name="Cleaned Data",
    )
    edl.connect(
        pipeline_name="Wind Power Forecasting",
        parent_name="Penmanshiel Torch Dataset Class",
        target_name="Main",
    )
    edl.connect(
        pipeline_name="Wind Power Forecasting",
        parent_name="MLP",
        target_name="Main",
    )
    edl.connect(
        pipeline_name="Wind Power Forecasting",
        parent_name="MLP Hyperparameters",
        target_name="Main",
    )

    if args.model == "mlp":
        torch.save(model, "usecases/wpf/models/MLP.pth")
        print("Model saved.")


if __name__ == "__main__":
    main()
