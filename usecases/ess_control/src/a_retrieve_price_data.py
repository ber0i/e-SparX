"""
Day-ahead price data download from the ENTSO-E Transparency Platform:

To download any available data from the ENTSO-E transpareny platform,
one can directly download data sets from the website (which does not work very well),
or use their API.
To make API calls, one first must create an account and then request a personal security token,
as explained here: https://uat-transparency.entsoe.eu/content/static_content/Static%20content/web%20api/how_to_get_security_token.html
To run this script, define your token in toolbox/api_token.py as follows:
api_token = <your token>
"""

import os

import esparx
import pandas as pd
from entsoe import EntsoePandasClient
from toolbox import api_token

data_path = "usecases/ess_control/data"

# check whether data had already been retrieved
if os.path.exists(os.path.join(data_path, "day_ahead_prices.csv")):

    # if yes, load data
    print("Data already retrieved. Loading as pandas DataFrame.")
    df = pd.read_csv(
        os.path.join(data_path, "day_ahead_prices.csv"), index_col=0, parse_dates=True
    )
    print("Done.")

else:

    mykey = api_token
    client = EntsoePandasClient(api_key=mykey)

    start = pd.Timestamp("20220101", tz="Europe/London")
    end = pd.Timestamp("20230101", tz="Europe/London")

    # Ireland and Northern Ireland Single Electricity Market (SEM) bidding zone (IE_SEM)
    df = client.query_day_ahead_prices(country_code="IE_SEM", start=start, end=end)

    df = pd.DataFrame(df, columns=["Price [EUR/MWh]"])
    df.index = df.index.tz_localize(None)
    df.index.name = "timestamp"
    df[:-1].to_csv(os.path.join(data_path, "day_ahead_prices.csv"))

# register this script in e-SparX
print(">>>>>>>>>>Registering this data retrieval script in e-SparX<<<<<<<<<<")
esparx.register_code(
    name="Retrieve ENTSO-E Price Data",
    description="Retrieve Irish day-ahead electricity prices from the ENTSO-E Transparency Platform.",
    file_type="PY",
    source_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/blob/main/usecases/ess_control/src/a_retrieve_price_data.py",
    download_url="https://gitlab.lrz.de/EMT/projects/edl-projects/registry-mvp/-/raw/main/usecases/ess_control/src/a_retrieve_price_data.py?inline=false",
    pipeline_name="Wind Farm ESS Control",
)

# register data in e-SparX
print(">>>>>>>>>>Registering data in e-SparX<<<<<<<<<<")
esparx.register_dataset_pandas(
    name="Day-Ahead Electricity Price Data",
    description="Hourly day-ahead electricity prices for the Irish SEM bidding zone.",
    file_type="CSV",
    df=df,
    source_url="https://newtransparency.entsoe.eu/market/energyPrices",
    pipeline_name="Wind Farm ESS Control",
    source_name="Retrieve ENTSO-E Price Data",
)
