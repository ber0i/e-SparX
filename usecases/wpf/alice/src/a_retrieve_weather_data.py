"""
Retrieve historical weather data and historical weather forecast data from
the Open-Meteo.com Weather API.
(Zippenfenig, P. (2023). Open-Meteo.com Weather API [Computer software].
Zenodo. https://doi.org/10.5281/ZENODO.7970649)

We set the location to the Penmanshiel wind farm, where we use the coordinates
as stated here: https://www.thewindpower.net/windfarm_en_23147_penmanshiel.php.

The forecast model used is GFS Global, which has a spatial resolution of 0.11° (~13 km),
a temporal resolution of 1h, and an update frequency of 6h
(see https://open-meteo.com/en/docs/historical-forecast-api). The model is run four times a day,
producing forecasts up to 16 days in advance
(see https://www.emc.ncep.noaa.gov/emc/pages/numerical_forecast_systems/gfs.php).
GFS model cycle runtime: 00, 06, 12, 18 (see https://www.nco.ncep.noaa.gov/pmb/products/gfs/#GFS).
"""

import os

import energydatalab as edl
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

processed_data_path = "usecases/wpf/alice/data/processed"

# check whether data had already been retrieved
if os.path.exists(
    os.path.join(processed_data_path, "Hist_Weather.csv")
) and os.path.exists(os.path.join(processed_data_path, "Hist_Forecast.csv")):

    # if yes, load data
    print("Data already retrieved. Loading as pandas DataFrame.")
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
    print("Done.")

else:

    # Latitude, Longitude
    latitude = 55.871333
    longitude = -2.354500
    # start, end
    start = "2022-01-01"
    end = "2023-01-01"

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    print("Retrieving historical weather forecast data.")
    # Set API URL and variables
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start,
        "end_date": end,
        "hourly": ["wind_speed_80m", "wind_direction_80m"],
        "wind_speed_unit": "ms",
        "timezone": "Europe/London",
        "models": "gfs_global",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process location
    response = responses[0]

    # Process hourly data
    hourly = response.Hourly()
    hourly_wind_speed_80m = hourly.Variables(0).ValuesAsNumpy()
    hourly_wind_direction_80m = hourly.Variables(1).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }
    hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
    hourly_data["wind_direction_80m"] = hourly_wind_direction_80m

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    print("Done.")

    # drop all rows where the "date" column does not start with "2022"
    df_hist_forecast = hourly_dataframe[hourly_dataframe["date"].dt.year == 2022]

    print("Retrieving historical weather data.")
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=-1)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # set URL and variables
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "start_date": "2021-12-31",
        "end_date": "2023-01-01",
        "hourly": [
            "wind_speed_10m",
            "wind_speed_100m",
            "wind_speed_80m",
            "wind_direction_10m",
            "wind_direction_100m",
            "wind_direction_80m",
        ],
        "wind_speed_unit": "ms",
        "timezone": "Europe/London",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process location
    response = responses[0]

    # Process hourly data
    hourly = response.Hourly()
    hourly_wind_speed_10m = hourly.Variables(0).ValuesAsNumpy()
    hourly_wind_speed_100m = hourly.Variables(1).ValuesAsNumpy()
    hourly_wind_speed_80m = hourly.Variables(2).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_direction_100m = hourly.Variables(4).ValuesAsNumpy()
    hourly_wind_direction_80m = hourly.Variables(5).ValuesAsNumpy()

    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )
    }
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_speed_100m"] = hourly_wind_speed_100m
    hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m
    hourly_data["wind_direction_100m"] = hourly_wind_direction_100m
    hourly_data["wind_direction_80m"] = hourly_wind_direction_80m

    hourly_dataframe_actual = pd.DataFrame(data=hourly_data)
    print("Done.")

    df_hist_weather = hourly_dataframe_actual[
        hourly_dataframe_actual["date"].dt.year == 2022
    ]

    # save to CSV
    print("Saving data to CSV.")
    df_hist_forecast.to_csv(
        os.path.join(processed_data_path, "Hist_Forecast.csv"), index=False
    )
    df_hist_weather.to_csv(
        os.path.join(processed_data_path, "Hist_Weather.csv"), index=False
    )
    print("Done.")


# register this script in EDL
print(">>>>>>>>>>Registering this data retrieval script in EDL<<<<<<<<<<")
edl.register_code(
    name="Retrieve Historical Weather Data",
    description="Retrieve historical weather data and historical weather forecast data from the Open-Meteo.com Weather API and save to CSV.",
    file_type="PY",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/wpf/alice/src/a_retrieve_weather_data.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/wpf/alice/src/a_retrieve_weather_data.py?inline=false",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
)

# register data in EDL
print(">>>>>>>>>>Registering data in EDL<<<<<<<<<<")
edl.register_data_pandas(
    name="Historical Weather Forecast Data",
    description="Historical weather forecasts (Model: GFS Global) at the Penmanshiel wind farm in 2022.",
    file_type="CSV",
    df=df_hist_forecast,
    source_url="https://open-meteo.com/en/docs/historical-forecast-api",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    parent_name="Retrieve Historical Weather Data",
)
edl.register_data_pandas(
    name="Historical Weather Data",
    description="Historical weather data at the Penmanshiel wind farm in 2022.",
    file_type="CSV",
    df=df_hist_weather,
    source_url="https://open-meteo.com/en/docs/historical-weather-api",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    parent_name="Retrieve Historical Weather Data",
)

print("Script finished.")
