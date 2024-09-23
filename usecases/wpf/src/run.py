import argparse

import mlflow
import torch
import wandb
from data.datasets import PenmanshielDataset
from mlflow.models import infer_signature
from models.architectures import mlp
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
        default=5,
        help="Number of epochs to train the model. Default: 5.",
    )
    args = parser.parse_args()

    # Data Preparation

    dataset = PenmanshielDataset(
        data_file="usecases/wpf/data/cleaned/Cleaned_Data.csv",
        lookback_timesteps=args.lookback_timesteps,
        forecast_timesteps=args.forecast_timesteps,
    )

    n = len(dataset)
    # TODO: REMOVE THIS LINE (FOR DEBUGGING PURPOSES ONLY)
    n = 1000
    n_train = int(0.7 * n)  # 70% for training
    n_val = int(0.15 * n)  # 15% for validation
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
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    if args.wandb:
        wandb.init(
            project=args.wandb_project_name,
            name=f"{args.model}_{args.lookback_timesteps}_{args.forecast_timesteps}",
        )

    for epoch in range(args.n_epochs):
        model.train()
        loss_list = []
        for batch, (X, y) in enumerate(loader_train):
            X = X.to(device=args.device)
            y = y.to(device=args.device)
            optimizer.zero_grad()
            y_pred = model(X)
            loss = torch.nn.MSELoss()(y_pred, y)
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
            loss = torch.nn.MSELoss()(y_pred, y)
            loss_list.append(loss.cpu().item())

        print(f"Epoch {epoch}, val MSE: {sum(loss_list)/len(loss_list):.4f}")
        if args.wandb:
            wandb.log({"val_mse": sum(loss_list) / len(loss_list)})

    if args.wandb:
        wandb.finish()

    signature = infer_signature(X.numpy(), model(X).detach().numpy())
    mlflow.pytorch.log_model(model, args.model, signature=signature)


if __name__ == "__main__":
    main()
