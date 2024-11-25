import json
import os
from types import SimpleNamespace

import esparx
import pandas as pd
from alice.src.datasets import PenmanshielDataset
from alice.src.models import lstm, mlp
from torch.utils.data import DataLoader

processed_data_path = "usecases/wpf/alice/data/processed"
cleaned_data_path = "usecases/wpf/alice/data/cleaned"
df_hist_weather = pd.read_csv(
    os.path.join(processed_data_path, "Hist_Weather.csv"),
    index_col=0,
    parse_dates=True,
)
df_hist_forecast = pd.read_csv(
    os.path.join(processed_data_path, "Hist_Forecast.csv"),
    index_col=0,
    parse_dates=True,
)
df = pd.read_csv(
    os.path.join(processed_data_path, "Penmanshiel_SCADA_2022.csv"), index_col=0
)
df_final = pd.read_csv(
    os.path.join(cleaned_data_path, "Cleaned_Data.csv"), index_col=0, parse_dates=True
)
with open("usecases/wpf/alice/hyperparameters/mlp.json", "r") as f:
    hp_mlp = json.load(f)
with open("usecases/wpf/alice/hyperparameters/lstm.json", "r") as f:
    hp_lstm = json.load(f)
args_mlp = SimpleNamespace(**hp_mlp)
model_mlp = mlp.Model(args_mlp)
args_lstm = SimpleNamespace(**hp_lstm)
model_lstm = lstm.Model(args_lstm)
dataset = PenmanshielDataset(
    data_file="usecases/wpf/alice/data/cleaned/Cleaned_Data.csv",
    lookback_timesteps=args_mlp.lookback_timesteps,
    forecast_timesteps=args_mlp.forecast_timesteps,
)
loader = DataLoader(dataset, batch_size=args_mlp.batch_size)
esparx.register_code(
    name="Retrieve Historical Weather Data",
    description="Retrieve historical weather data and historical weather forecast data from the Open-Meteo.com Weather API and save to CSV.",
    file_type="PY",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/src/a_retrieve_weather_data.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/src/a_retrieve_weather_data.py?inline=false",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
)
esparx.register_dataset_pandas(
    name="Historical Weather Forecast Data",
    description="Historical weather forecasts (Model: GFS Global) at the Penmanshiel wind farm in 2022.",
    file_type="CSV",
    df=df_hist_forecast,
    source_url="https://open-meteo.com/en/docs/historical-forecast-api",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Retrieve Historical Weather Data",
)
esparx.register_dataset_pandas(
    name="Historical Weather Data",
    description="Historical weather data at the Penmanshiel wind farm in 2022.",
    file_type="CSV",
    df=df_hist_weather,
    source_url="https://open-meteo.com/en/docs/historical-weather-api",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Retrieve Historical Weather Data",
)
esparx.register_dataset_free(
    name="Penmanshiel SCADA 2022 WT01-10",
    description="Raw Penmanshiel SCADA data from 2022, Turbine 01 to 10, downloaded from Zenodo as ZIP file.",
    file_type="ZIP",
    source_url="https://zenodo.org/records/8253010",
    download_url="https://zenodo.org/records/8253010/files/Penmanshiel_SCADA_2022_WT01-10_4462.zip?download=1",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
)
esparx.register_dataset_free(
    name="Penmanshiel SCADA 2022 WT11-15",
    description="Raw Penmanshiel SCADA data from 2022, Turbine 11 to 15, downloaded from Zenodo as ZIP file.",
    file_type="ZIP",
    source_url="https://zenodo.org/records/8253010",
    download_url="https://zenodo.org/records/8253010/files/Penmanshiel_SCADA_2022_WT11-15_4463.zip?download=1",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
)
esparx.register_dataset_pandas(
    name="Penmanshiel SCADA 2022",
    description="Processed Penmanshiel SCADA data from 2022, all turbines.",
    file_type="CSV",
    df=df,
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
)
esparx.register_code(
    name="Preprocess Raw Data",
    description="Extract relevant variables from raw SCADA data from Penmanshiel wind farm and save it to one CSV file.",
    file_type="PY",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/src/b_preprocess_power_data.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/src/b_preprocess_power_data.py?inline=false",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Penmanshiel SCADA 2022 WT01-10",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Penmanshiel SCADA 2022 WT11-15",
    target_name="Preprocess Raw Data",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Preprocess Raw Data",
    target_name="Penmanshiel SCADA 2022",
)
esparx.register_code(
    name="Clean and Normalize Data",
    description="Replace false measurements, min-max normalize data. Save cleaned data to one CSV file.",
    file_type="IPYNB",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/src/c_clean_norm_data.ipynb",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/src/c_clean_norm_data.ipynb?inline=false",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Penmanshiel SCADA 2022",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Historical Weather Forecast Data",
    target_name="Clean and Normalize Data",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Historical Weather Data",
    target_name="Clean and Normalize Data",
)
esparx.register_dataset_pandas(
    name="Cleaned Data",
    description="Contains features and target, cleaned and normalized.",
    file_type="CSV",
    df=df_final,
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Clean and Normalize Data",
)
esparx.register_code(
    name="Main",
    description="Script to train and evaluate a model for wind power forecasting.",
    file_type="PY",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/src/d_main.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/src/d_main.py?inline=false",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Cleaned Data",
)
esparx.register_hyperparameters(
    name="MLP Hyperparameters",
    description="Hyperparameters for the MLP model.",
    hyperparameters=hp_mlp,
    file_type="JSON",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/hyperparameters/mlp.json",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/hyperparameters/mlp.json?inline=false",  # noqa: E501
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
)
esparx.register_hyperparameters(
    name="LSTM Hyperparameters",
    description="Hyperparameters for the LSTM model.",
    hyperparameters=hp_lstm,
    file_type="JSON",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/hyperparameters/lstm.json",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/hyperparameters/lstm.json?inline=false",  # noqa: E501
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
)
esparx.register_code(
    name="Penmanshiel Torch Dataset Class",
    description="Code defining the PyTorch dataset class for the Penmanshiel dataset.",
    file_type="PY",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/src/datasets/penmanshiel.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/src/datasets/penmanshiel.py?inline=false",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
)
esparx.register_model_pytorch(
    name="MLP",
    description="PyTorch nn.Module class for an MLP wind power forecasting model.",
    file_type="PY",
    model=model_mlp,
    input_example=next(iter(loader))[0],
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/src/models/mlp.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/src/models/mlp.py?inline=false",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
)
esparx.register_model_pytorch(
    name="LSTM",
    description="PyTorch nn.Module class for an LSTM wind power forecasting model.",
    file_type="PY",
    model=model_lstm,
    input_example=next(iter(loader))[0],
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/src/models/lstm.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/src/models/lstm.py?inline=false",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
)
esparx.register_results(
    name="MLP Results",
    description="Error metric values of the MLP model on the test dataset.",
    results={
        "MSE": 0.01642,
        "RMSE": 0.12814,
    },
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Main",
)
esparx.register_results(
    name="LSTM Results",
    description="Error metric values of the LSTM model on the test dataset.",
    results={
        "MSE": 0.014245,
        "RMSE": 0.11935,
    },
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Main",
)
esparx.register_results(
    name="Persistence Results",
    description="Error metric values of the persistence model on the test dataset.",
    results={
        "MSE": 0.1275,
        "RMSE": 0.3571,
    },
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Main",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Penmanshiel Torch Dataset Class",
    target_name="Main",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="MLP",
    target_name="Main",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="LSTM",
    target_name="Main",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="MLP Hyperparameters",
    target_name="Main",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="LSTM Hyperparameters",
    target_name="Main",
)
esparx.register_parameters(
    name="MLP Parameters",
    description="Trained parameters of the MLP model.",
    file_type="PTH",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/models/MLP.pth",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/models/MLP.pth?inline=false",  # noqa: E501
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Main",
)
esparx.register_parameters(
    name="LSTM Parameters",
    description="Trained parameters of the LSTM model.",
    file_type="PTH",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/models/LSTM.pth",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/models/LSTM.pth?inline=false",  # noqa: E501
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Main",
)
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
    source_name="MLP",
    target_name="MLP/LSTM Hyperparameter Tuning",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="LSTM",
    target_name="MLP/LSTM Hyperparameter Tuning",
)
esparx.register_hyperparameters(
    name="MLP Tuned Hyperparameters",
    description="Hyperparameters for MLP after running a hyperparameter tuning.",
    hyperparameters={
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
    },
    file_type="JSON",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/hyperparameters/mlp_tuned.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/hyperparameters/mlp_tuned.py?inline=false",  # noqa: E501
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="MLP/LSTM Hyperparameter Tuning",
)
esparx.register_hyperparameters(
    name="LSTM Tuned Hyperparameters",
    description="Hyperparameters for LSTM after running a hyperparameter tuning.",
    hyperparameters={
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
    },
    file_type="JSON",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/hyperparameters/lstm_tuned.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/hyperparameters/lstm_tuned.py?inline=false",  # noqa: E501
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="MLP/LSTM Hyperparameter Tuning",
)
esparx.register_code(
    name="Main",
    description="Script to train and evaluate a model for wind power forecasting.",
    file_type="PY",
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="Cleaned Data",
)
esparx.register_results(
    name="MLP Results Tuned",
    description="Error metric values of the MLP model on the test dataset after hyperparameter tuning.",
    results={
        "MSE": 0.014492,
        "RMSE": 0.12038,
    },
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="Main",
)
esparx.register_results(
    name="LSTM Results Tuned",
    description="Error metric values of the LSTM model on the test dataset after hyperparameter tuning.",
    results={
        "MSE": 0.0136,
        "RMSE": 0.11662,
    },
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="Main",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="Penmanshiel Torch Dataset Class",
    target_name="Main",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="MLP",
    target_name="Main",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="LSTM",
    target_name="Main",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="MLP Tuned Hyperparameters",
    target_name="Main",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="LSTM Tuned Hyperparameters",
    target_name="Main",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="Main",
    target_name="Persistence Results",
)
esparx.register_parameters(
    name="MLP Parameters Tuned",
    description="Trained parameters of the MLP model with tuned hyperparameters.",
    file_type="PTH",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/models/MLP_tuned.pth",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/bob/models/MLP_tuned.pth?inline=false",  # noqa: E501
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="Main",
)
esparx.register_parameters(
    name="LSTM Parameters Tuned",
    description="Trained parameters of the LSTM model with tuned hyperparameters.",
    file_type="PTH",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/models/LSTM_tuned.pth",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/bob/models/LSTM_tuned.pth?inline=false",  # noqa: E501
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="Main",
)
esparx.register_code(
    name="TFT Hyperparameter Tuning",
    description="Hyperparameter tuning for the TFT model using Optuna",
    file_type="PY",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/src/b_hp_tuning_tft.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/bob/src/b_hp_tuning_tft.py?inline=false",
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="Cleaned Data",
)
esparx.register_hyperparameters(
    name="TFT Tuned Hyperparameters",
    description="Hyperparameters for the TFT model after tuning.",
    hyperparameters={
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
    },
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
esparx.register_code(
    name="TFT Training and Testing",
    description="Training and testing the TFT model from the Darts library.",
    file_type="PY",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/src/c_tft.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/bob/src/c_tft.py?inline=false",
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="Cleaned Data",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="TFT Tuned Hyperparameters",
    target_name="TFT Training and Testing",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="TFT",
    target_name="TFT Training and Testing",
)
esparx.register_results(
    name="TFT Results Tuned",
    description="Results of the TFT model with tuned hyperparameters.",
    results={"MSE": 0.012317246495134465, "RMSE": 0.11098309103},
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="TFT Training and Testing",
)
esparx.register_parameters(
    name="TFT Parameters Tuned",
    description="Trained parameters for the TFT model.",
    file_type="PKL",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/bob/models/tft/",
    pipeline_name="Wind Power Forecasting - TFT",
    source_name="TFT Training and Testing",
)
