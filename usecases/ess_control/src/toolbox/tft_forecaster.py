import logging
from datetime import timedelta

import numpy as np
import torch
import torch.nn as nn
from commonpower.data_forecasting.base import Forecaster
from darts import TimeSeries
from darts.models import TFTModel

logger = logging.getLogger("pytorch_lightning.utilities.rank_zero")


class IgnorePLFilter(logging.Filter):
    def filter(self, record):
        return "available:" not in record.getMessage()


logger.addFilter(IgnorePLFilter())


class TFTForecaster(Forecaster):
    def __init__(
        self,
        model_weights_path: str,
        max_power: float,
        frequency: timedelta = timedelta(minutes=10),
        horizon: timedelta = timedelta(minutes=10 * 6),
        look_back: timedelta = timedelta(minutes=10 * 12),
        hidden_size: int = 19,
        lstm_layers: int = 2,
        num_attention_heads: int = 2,
        dropout: float = 0.5,
        batch_size: int = 64,
    ):
        """
        TFT Forecaster.

        Args:
            model_weights_path (str): Path to the model weights, which had been trained offline.
            max_power (float): Maximum power value (required for min-max scaling of input data).
            frequency (timedelta, optional): Frequency of generated forecasts. Defaults to timedelta(hours=1).
            horizon (timedelta, optional): Horizon to generate forecasts for. Defaults to timedelta(hours=24).
            look_back (timedelta, optional): Look back period for the input data. Defaults to timedelta(hours=24).
            hidden_size (int, optional): Hidden size of the LSTM layers. Defaults to 19.
            lstm_layers (int, optional): Number of LSTM layers. Defaults to 2.
            num_attention_heads (int, optional): Number of attention heads. Defaults to 2.
            dropout (float, optional): Dropout rate. Defaults to 0.5.
        """

        super().__init__(frequency=frequency, horizon=horizon, look_back=look_back)

        self.model_output_steps = 6  # known for the TFT model used here
        self.lookback_timesteps = int(look_back / frequency)
        if self.lookback_timesteps != 12:
            raise ValueError("Lookback must be 2 hours for TFT model.")
        self.forecast_timesteps = int(horizon / frequency)
        self.iteration_steps = (horizon // frequency) // self.model_output_steps
        self.max_power = max_power

        model = TFTModel(
            input_chunk_length=self.lookback_timesteps,
            output_chunk_length=self.model_output_steps,
            hidden_size=hidden_size,
            lstm_layers=lstm_layers,
            num_attention_heads=num_attention_heads,
            dropout=dropout,
            batch_size=batch_size,
            n_epochs=30,
            add_relative_index=False,
            add_encoders=None,
            likelihood=None,
            loss_fn=nn.MSELoss(),
        )

        model.load_weights(model_weights_path, map_location=torch.device("cpu"))

        self.model = model

    @property
    def input_range(self) -> tuple[timedelta]:
        return (-(self.look_back - timedelta(minutes=10)), self.horizon)

    def __call__(self, data: np.ndarray) -> np.ndarray:
        """
        Make a forecast.

        Args:
            data (np.ndarray): Data of shape (self.lookback_timesteps + self.forecast_timesteps, n_vars).
            Expect n_vars = 5, where the first column is the power, the second and fourth are
            the historical weather data (wind speed and direction), and the third and fifth are
            the historical weather forecast data (wind speed and direction).

        Returns:
            np.ndarray: Forecast of shape (self.forecast_timesteps, n_vars).
        """

        target_col = 0
        hist_weather_cols = [1, 3]
        hist_forecast_cols = [2, 4]

        data_target = -data[: self.lookback_timesteps, target_col] / self.max_power
        data_target = -data[: self.lookback_timesteps, target_col] / self.max_power
        data_hist_col0 = data_target.reshape(-1, 1)
        data_hist_col12 = data[: self.lookback_timesteps, hist_weather_cols]
        data_hist = np.concatenate([data_hist_col0, data_hist_col12], axis=1)
        data_forecast = data[
            : self.lookback_timesteps + self.model_output_steps, hist_forecast_cols
        ]

        target = TimeSeries.from_values(data_target)
        p_cov = TimeSeries.from_values(data_hist)
        f_cov = TimeSeries.from_values(data_forecast)

        if len(data) != self.lookback_timesteps + self.forecast_timesteps:

            print("Not sufficient future data points available. Using persistence forecast.")
            pred_power = np.array([target.last_value()]*self.forecast_timesteps)

        else:

            # predict first window
            pred_power = (
                self.model.predict(
                    n=self.model_output_steps,
                    series=target,
                    past_covariates=p_cov,
                    future_covariates=f_cov,
                    verbose=False,
                    show_warnings=False,
                )
                .values()
                .flatten()
            )

            for step in range(1, self.iteration_steps):
                data_target = np.concatenate(
                    [
                        data_target[self.model_output_steps :],
                        pred_power[-self.model_output_steps :],
                    ]
                )
                target = TimeSeries.from_values(data_target)
                # for iterative forecasting, we do not have historical weather data
                # we use the historical weather forecast data instead
                # the first colum of data_hist is the target though, so here we can use the produced forecast
                data_hist_col0 = data_target.reshape(-1, 1)
                data_hist_col12 = data[
                    self.model_output_steps * step : self.model_output_steps * step
                    + self.lookback_timesteps,
                    hist_forecast_cols,
                ]
                data_hist = np.concatenate([data_hist_col0, data_hist_col12], axis=1)
                p_cov = TimeSeries.from_values(data_hist)
                data_forecast = data[
                    self.model_output_steps * step : self.model_output_steps * (step + 1)
                    + self.lookback_timesteps,
                    hist_forecast_cols,
                ]
                f_cov = TimeSeries.from_values(data_forecast)

                # predict next window
                pred_power_tmp = (
                    self.model.predict(
                        n=self.model_output_steps,
                        series=target,
                        past_covariates=p_cov,
                        future_covariates=f_cov,
                        verbose=False,
                        show_warnings=False,
                    )
                    .values()
                    .flatten()
                )

                # concatenate predictions
                pred_power = np.concatenate([pred_power, pred_power_tmp])

        # scale back to negative power values
        pred_power = -pred_power * self.max_power
            
        # set positive values (negative power predictions) to zero
        pred_power[pred_power > 0] = 0
        pred_power = pred_power.reshape(-1, 1)

        return pred_power
