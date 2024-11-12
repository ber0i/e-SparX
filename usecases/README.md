# EDL Use Cases

This folder holds two usecases from energy research with real data. All models where actually trained and results are real. This will give you an understanding of how you can use the EDL in realistic ML projects!

## Wind Power Forecasting (WPF)

**Objective**: Produce farm-level wind power forecasts (i.e., one time series) for the Penmanshiel wind farm. Forecasting horizon: 1h, multi-step, 10min resolution (i.e., one forecast consists of six values).

To produce one forecast for $t+1,\dots,t+6$, the input features are:

- historical wind power, speed, and wind direction data 2h back: $t-11,\dots,t$
- hourly wind speed and direction forecasts for the forecasting horizon, linearly interpolated to 10min resoltuion for $t+1,\dots,t+6$

Weather data is taken from Open Meteo. Wind power data is taken from Zenodo.

We assume that the researcher Alice implements a Multilayer Perceptron (MLP) and Long Short-Term Memory (LSTM). Later, the researcher Bob reuses her artifacts, adds hyperparameter tuning (which improves Alice's previous results) and implements a Temporal Fusion Transformer (TFT), which outperforms Alice's models.

## Energy Storage System (ESS) Control

**Objective**: Optimally control an ESS in the setting of a wind farm, which can either sell produced electricity to the grid or load it to its ESS. The objective is to maximize the wind farm's profit.

For the implementation, we use the [commonpower](https://github.com/TUMcps/commonpower) framework. At each time step, the given information is
- current wind power production and wind power production forecasts
- current electricity wholesale market price and price forecasts
- current ESS state of charge

We again use data from the penmanshiel wind farm, so we can reuse the data pipeline from the first use case. To produce the forecasts, we use the best-performing forecaster from the first usecase, the TFT.

We train a reinforcement learning controller using the PPO Algorithm. This algorithm is benchmarked with optimal control.

