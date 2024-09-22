# EDL Use Cases

## Wind Power Forecasting

Objective: Farm-level forecasts (i.e., one time series) for the Penmanshiel wind farm. Forecasting horizon: 1h, multi-step, 10min resolution (i.e., one forecast consists of six values).

To produce one forecast for $t+1,\dots,t+6$, the input features are:

- historical wind power, speed, and wind direction data 2h back: $t-11,\dots,t$
- hourly wind speed and direction forecasts for the forecasting horizon, linearly interpolated to 10min resoltuion for $t+1,\dots,t+6$

Weather data is taken from Open Meteo. Wind power data is taken from Zenodo.

### Acknowledgements

We appreciate the following GitHub repository for its publicly available code and methods, which we use as example models:

https://github.com/LarsBentsen/FFTransformer

