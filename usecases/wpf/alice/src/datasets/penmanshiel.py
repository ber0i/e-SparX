import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


class PenmanshielDataset(Dataset):
    def __init__(
        self,
        data_file,
        lookback_timesteps=12,
        forecast_timesteps=6,
        transform=None,
        target_transform=None,
    ):
        self.dataset = pd.read_csv(data_file, index_col=0, parse_dates=True)
        self.lookback_timesteps = lookback_timesteps
        self.forecast_timesteps = forecast_timesteps
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return (
            len(self.dataset) - (self.lookback_timesteps + self.forecast_timesteps) + 1
        )

    def __getitem__(self, idx):
        idx_hist = self.dataset.index[idx : idx + self.lookback_timesteps]
        idx_forecast = self.dataset.index[
            idx
            + self.lookback_timesteps : idx
            + self.lookback_timesteps
            + self.forecast_timesteps
        ]
        array_hist = np.array(
            [
                self.dataset.loc[
                    idx_hist, ["Power (kW)", "Wind Speed (m/s)", "Wind Direction (°)"]
                ].values
            ]
        ).reshape(self.lookback_timesteps * 3)
        array_forecast = np.array(
            [
                self.dataset.loc[
                    idx_forecast,
                    ["Wind Speed Forecast (m/s)", "Wind Direction Forecast (°)"],
                ].values
            ]
        ).reshape(self.forecast_timesteps * 2)
        array_hist_forecast = np.concatenate((array_hist, array_forecast), axis=0)
        x = torch.tensor(array_hist_forecast, dtype=torch.float32)
        array_target = np.array(
            [self.dataset.loc[idx_forecast, ["Power (kW)"]].values]
        ).reshape(self.forecast_timesteps)
        y = torch.tensor(array_target, dtype=torch.float32)
        if self.transform:
            x = self.transform(x)
        if self.target_transform:
            y = self.target_transform(y)
        return x, y