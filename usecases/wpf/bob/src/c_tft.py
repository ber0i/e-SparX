import argparse
import json
import os

import esparx
import pandas as pd
import torch.nn as nn
from darts import TimeSeries
from darts.metrics import mse, rmse
from darts.models import TFTModel
from pytorch_lightning.callbacks import EarlyStopping

# warnings.filterwarnings("ignore")


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
        name="Train and Test TFT",
        description="Training and testing the TFT model from the Darts library.",
        file_type="PY",
        source_url="https://gitlab.lrz.de/energy-management-technologies-public/e-sparx/-/blob/main/usecases/wpf/bob/src/c_tft.py",
        download_url="https://gitlab.lrz.de/energy-management-technologies-public/e-sparx/-/raw/main/usecases/wpf/bob/src/c_tft.py?inline=false",
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="Cleaned SCADA and Weather Data",
    )
    esparx.connect(
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="TFT Tuned Hyperparameters",
        target_name="Train and Test TFT",
    )
    esparx.connect(
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="TFT",
        target_name="Train and Test TFT",
    )

    project_base_path = os.getcwd()

    datafile = os.path.join(
        project_base_path,
        "usecases/wpf/bob/esparx_artifacts/datasets/Cleaned_Data.csv",
    )
    hpfile = os.path.join(
        project_base_path, "usecases/wpf/bob/hyperparameters/tft_tuned.json"
    )

    with open(hpfile, "r") as f:
        hp = json.load(f)

    for key, value in hp.items():
        setattr(args, key, value)

    if not args.demo:

        df = pd.read_csv(datafile)

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
        train_size = int(args.train_share * n)
        val_size = int(args.val_share * n)

        # Splitting the data
        p_train = p_cov[:train_size]
        f_train = f_cov[:train_size]
        y_train = target[:train_size]
        p_val = p_cov[train_size : train_size + val_size]
        f_val = f_cov[train_size : train_size + val_size]
        y_val = target[train_size : train_size + val_size]
        p_test = p_cov[train_size + val_size :]
        f_test = f_cov[train_size + val_size :]
        y_test = target[train_size + val_size :]

        # early stop callback
        my_stopper = EarlyStopping(monitor="val_loss", patience=args.n_epochs / 3)
        pl_trainer_kwargs = {
            "callbacks": [my_stopper],
            "devices": [0],
            "accelerator": "cuda",
        }

        model = TFTModel(
            input_chunk_length=args.lookback_timesteps,
            output_chunk_length=args.forecast_timesteps,
            hidden_size=args.hidden_size,
            lstm_layers=args.lstm_layers,
            num_attention_heads=args.num_attention_heads,
            dropout=args.dropout,
            batch_size=args.batch_size,
            n_epochs=args.n_epochs,
            add_relative_index=False,
            add_encoders=None,
            likelihood=None,  # QuantileRegression is set per default
            loss_fn=nn.MSELoss(),
            pl_trainer_kwargs=pl_trainer_kwargs,
            optimizer_kwargs={"lr": args.learning_rate},
            random_state=42,
        )

        # Training the model
        model.fit(
            series=y_train,
            past_covariates=p_train,
            future_covariates=f_train,
            val_series=y_val,
            val_past_covariates=p_val,
            val_future_covariates=f_val,
            verbose=False,
        )

        model.save(
            os.path.join(
                project_base_path,
                "usecases/wpf/bob/models/tft/tft.pkl",
            )
        )

        p_test_withinput = p_val[-args.lookback_timesteps :].append(p_test)
        f_test_withinput = f_val[-args.lookback_timesteps :].append(f_test)
        y_test_withval = y_val.append(y_test)

        # generating predictions on the test set and evaluating each window separately
        num_windows = len(y_test) - args.forecast_timesteps + 1
        print(f"Number of windows: {num_windows}")
        rmse_list = []
        mse_list = []

        for i in range(num_windows):
            print(f"forecasting window {i}")
            forecast = model.predict(
                n=args.forecast_timesteps,
                series=y_test_withval[: val_size + i],
                past_covariates=p_test_withinput,
                future_covariates=f_test_withinput,
            )
            rmse_list.append(rmse(y_test[i : i + args.forecast_timesteps], forecast))
            mse_list.append(mse(y_test[i : i + args.forecast_timesteps], forecast))

        rmse_overall = sum(rmse_list) / num_windows
        print(f"test RMSE: {rmse_overall}")
        mse_overall = sum(mse_list) / num_windows
        print(f"test MSE: {mse_overall}")

        esparx.register_results(
            name="TFT Test MSE and RMSE Tuned",
            description="Results of the TFT model with tuned hyperparameters.",
            results={"MSE": mse_overall, "RMSE": rmse_overall},
            pipeline_name="Wind Power Forecasting - TFT",
            source_name="Train and Test TFT",
        )

    else:

        print("Running in demo mode. Registering mock results.")
        mock_results = {"MSE": 0.012317246495134465, "RMSE": 0.11098309103}
        esparx.register_results(
            name="TFT Test MSE and RMSE Tuned",
            description="Results of the TFT model with tuned hyperparameters.",
            results=mock_results,
            pipeline_name="Wind Power Forecasting - TFT",
            source_name="Train and Test TFT",
        )

    esparx.register_parameters(
        name="TFT Parameters Tuned",
        description="Trained parameters for the TFT model.",
        file_type="PKL",
        source_url="https://gitlab.lrz.de/energy-management-technologies-public/e-sparx/-/blob/main/usecases/wpf/bob/models/tft/",
        pipeline_name="Wind Power Forecasting - TFT",
        source_name="Train and Test TFT",
    )


if __name__ == "__main__":
    main()
