import argparse
import json
import os

import esparx
import optuna
import pandas as pd
import torch
import torch.nn as nn
from darts import TimeSeries
from darts.metrics import mse
from darts.models import TFTModel
from optuna import Trial
from pytorch_lightning.callbacks import EarlyStopping


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
    args = parser.parse_args()

    esparx.register_code(
        name="TFT Hyperparameter Tuning",
        description="Hyperparameter tuning for the TFT model using Optuna",
        file_type="PY",
        source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/src/b_hp_tuning_tft.py",
        download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/bob/src/b_hp_tuning_tft.py?inline=false",
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="Cleaned SCADA and Weather Data",
    )

    project_base_path = os.getcwd()

    if not args.demo:

        # Set the precision of the matrix multiplication to medium (for speed up)
        torch.set_float32_matmul_precision("medium")

        datapath = os.path.join(
            project_base_path,
            "usecases/wpf/bob/esparx_artifacts/datasets/Cleaned_Data.csv",
        )
        hppath = os.path.join(
            project_base_path, "usecases/wpf/bob/hyperparameters/tft_tuned.json"
        )
        df = pd.read_csv(datapath)

        # create df for future features
        df_fcovs = df[["Wind Speed Forecast (m/s)", "Wind Direction Forecast (°)"]]
        # set future covariates
        f_cov = TimeSeries.from_series(df_fcovs)

        # set  target column
        target = TimeSeries.from_series(df["Power (kW)"])

        # set remaining variables to past features
        p_cov = TimeSeries.from_series(
            df[["Power (kW)", "Wind Speed (m/s)", "Wind Direction (°)"]]
        )

        n = int(len(df))
        train_size = int(0.7 * n)
        val_size = int(0.15 * n)

        # Splitting the data
        p_train = p_cov[:train_size]
        f_train = f_cov[:train_size]
        y_train = target[:train_size]
        p_val = p_cov[train_size : train_size + val_size]
        f_val = f_cov[train_size : train_size + val_size]
        y_val = target[train_size : train_size + val_size]

        # Define the objective function for Optuna

        forecast_horizon = 6

        def objective(trial: Trial):

            # Defining the hyperparameter search space

            hidden_size = trial.suggest_int(
                "hidden_size", 8, 32
            )  # number of neurons in each hidden layer
            lstm_layers = trial.suggest_int("lstm_layers", 1, 2)
            num_attention_heads = trial.suggest_int("num_attention_heads", 1, 4)
            dropout = trial.suggest_categorical(
                "dropout", [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
            )
            batch_size = trial.suggest_categorical("batch_size", [32, 64])
            learning_rate = trial.suggest_float("learning_rate", 1e-5, 1e-3, log=True)

            my_stopper = EarlyStopping(monitor="val_loss", patience=50 / 3)
            # early stopping enables finishing training early if (in our case) the val_loss is not improving after 10 epochs

            pl_trainer_kwargs = {
                "callbacks": [my_stopper],
                # "accelerator": "cuda",  # connects Lightning trainer to GPU
            }

            # Create the TFTModel with the selected hyperparameters
            model = TFTModel(
                input_chunk_length=12,
                output_chunk_length=forecast_horizon,
                hidden_size=hidden_size,
                lstm_layers=lstm_layers,
                num_attention_heads=num_attention_heads,
                dropout=dropout,
                batch_size=batch_size,
                n_epochs=50,
                loss_fn=nn.MSELoss(),  # loss used for training. this choice makes model deterministic
                pl_trainer_kwargs=pl_trainer_kwargs,
                optimizer_kwargs={"lr": learning_rate},
            )

            # Train the model
            model.fit(
                series=y_train,
                past_covariates=p_train,
                future_covariates=f_train,
                val_series=y_val,
                val_past_covariates=p_val,
                val_future_covariates=f_val,
                verbose=True,
            )

            # Make predictions on the validation set
            p_val_withinput = p_train[-12:].append(
                p_val
            )  # append past input to val set
            f_val_withinput = f_train[-12:].append(f_val)

            val_forecast = model.predict(
                n=len(y_val),
                past_covariates=p_val_withinput,
                future_covariates=f_val_withinput,
            )

            # Evaluate the model using MSE
            mse_score = mse(y_val, val_forecast)

            return mse_score

        # set and run the hyperparameter optimization using Optuna
        study = optuna.create_study(direction="minimize")
        study.optimize(objective, n_trials=2)

        # Get the best hyperparameters and best MSE score
        best_params = study.best_params
        best_mse = study.best_value

        # fixed hyperparameters
        hp_dict = {
            "lookback_timesteps": 12,
            "forecast_timesteps": 6,
            "n_epochs": 30,
            "train_share": 0.7,
            "val_share": 0.15,
            "test_share": 0.15,
            "train_loss_fn": "mse",
        }

        print("Best Hyperparameters:")
        for param, value in best_params.items():
            print(f"{param}: {value}")
            if param != "Best MSE":
                hp_dict[f"{param}"] = value

        # Saving the besthyperparameters to a file
        with open(hppath, "w") as json_file:
            json.dump(hp_dict, json_file)

        esparx.register_hyperparameters(
            name="TFT Tuned Hyperparameters",
            description="Hyperparameters for the TFT model after tuning.",
            hyperparameters=hp_dict,
            file_type="JSON",
            source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/hyperparameters/tft_tuned.json",
            download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/bob/hyperparameters/tft_tuned.json?inline=false",
            pipeline_name="Wind Power Forecasting - TFT",
            source_name="TFT Hyperparameter Tuning",
        )

        print(f"Best MSE: {best_mse}")

    else:

        print("Running in demo mode, registering mock hyperparameters")
        mock_hp = {
            "lookback_timesteps": 12,
            "forecast_timesteps": 6,
            "n_epochs": 30,
            "train_share": 0.7,
            "val_share": 0.15,
            "test_share": 0.15,
            "train_loss_fn": "mse",
            "hidden_size": 19,
            "lstm_layers": 2,
            "num_attention_heads": 2,
            "dropout": 0.5,
            "batch_size": 64,
            "learning_rate": 0.000489035986513014,
        }
        esparx.register_hyperparameters(
            name="TFT Tuned Hyperparameters",
            description="Hyperparameters for the TFT model after tuning.",
            hyperparameters=mock_hp,
            file_type="JSON",
            source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/hyperparameters/tft_tuned.json",
            download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/bob/hyperparameters/tft_tuned.json?inline=false",
            pipeline_name="Wind Power Forecasting - TFT",
            source_name="TFT Hyperparameter Tuning",
        )

        esparx.register_model_free(
            name="TFT",
            description="Transformer-based time series forecasting model for wind power forecasting.",
            file_type="none",
            flavor="Darts",
            pipeline_name="Wind Power Forecasting - TFT",
        )
        esparx.connect(
            pipeline_name="Wind Power Forecasting - TFT",
            source_name="TFT",
            target_name="TFT Hyperparameter Tuning",
        )


if __name__ == "__main__":
    main()
