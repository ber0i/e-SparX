import json
import pathlib
from datetime import timedelta

from commonpower.core import System
from commonpower.data_forecasting.base import DataProvider
from commonpower.data_forecasting.data_sources import CSVDataSource
from commonpower.data_forecasting.forecasters import PerfectKnowledgeForecaster
from commonpower.models.buses import ExternalGrid, RTPricedBusLinear
from commonpower.models.components import ESS, RenewableGen
from commonpower.models.powerflow import PowerBalanceModel
from commonpower.modeling.param_initialization import RangeInitializer

# Local imports
from .tft_forecaster import TFTForecaster


def setup_system(
    data_path: pathlib.Path,
    esparx_data_path: pathlib.Path,
    model_weights_path: pathlib.Path,
    hp_file_path: pathlib.Path,
    forecast_frequency: timedelta,
    forecast_horizon: timedelta,
    lookback_horizon: timedelta,
):

    with open(f"{hp_file_path}/tft_tuned.json", "r") as f:
        hp = json.load(f)

    # set data sources
    # the power data had been min-max scaled, we will back-transform it to kW (note that min_power = 0)
    max_power = 28856.585504080267

    wp_data = CSVDataSource(
        esparx_data_path / "Cleaned_Data.csv",
        delimiter=",",
        datetime_format="%Y-%m-%d %H:%M:%S",
        rename_dict={"timestamp": "t", "Power (kW)": "p"},
        auto_drop=False,
        resample=forecast_frequency,
    ).apply_to_column(
        "p", lambda x: -x * max_power
    )  # provided power must be negative and scaled to kW
    # the remaining columns are kept as they are required for the forecaster

    price_data = CSVDataSource(
        data_path / "day_ahead_prices.csv",
        delimiter=",",
        datetime_format="%Y-%m-%d %H:%M:%S",
        rename_dict={"timestamp": "t", "Price [EUR/MWh]": "psi"},
        auto_drop=True,
        resample=forecast_frequency,
    ).apply_to_column(
        "psi", lambda x: x / 1000
    )  # convert to EUR/kWh

    forecaster = TFTForecaster(
        model_weights_path=f"{model_weights_path}/tft.pkl",
        max_power=max_power,
        frequency=forecast_frequency,
        horizon=forecast_horizon,
        look_back=lookback_horizon,
        hidden_size=hp["hidden_size"],
        lstm_layers=hp["lstm_layers"],
        num_attention_heads=hp["num_attention_heads"],
        dropout=hp["dropout"],
        batch_size=hp["batch_size"],
    )

    wp_data_provider = DataProvider(
        wp_data,
        forecaster,
        observable_features=["p"],
    )
    price_data_provider = DataProvider(
        price_data,
        PerfectKnowledgeForecaster(
            frequency=forecast_frequency, horizon=forecast_horizon
        ),
    )

    # wind farm bus
    farm = RTPricedBusLinear("Farm", config={"p": (-1e8, 0)}).add_data_provider(
        price_data_provider
    )

    # external grid bus
    grid = ExternalGrid("Grid")

    # ess component
    # penmanshiel wind farm has an installed capacity of ~ 30MW (see https://www.energymap.co.uk/project.asp?pageid=2939)
    capacity = 300  # kWh (=0.3MWh)
    ess = ESS(
        "ESS",
        {
            "rho": 0.001,  # charging/discharging 1 kWh incurs a cost of wear of 0.001
            "p": (-50, 50),  # active power limits
            "q": (0, 0),  # reactive power limits
            "etac": 0.98,  # charging efficiency
            "etad": 0.98,  # discharging efficiency
            "etas": 1,  # self-discharge (after one time step 100% of the soc is left -> no self-discharge)
            "soc": (0.1 * capacity, 0.9 * capacity),  # soc limits
            "soc_init": RangeInitializer(
                lb=0.1 * capacity, ub=0.9 * capacity
            ),  # uniform sampling from [0.1, 0.9] * capacity
        },
    )

    # wind power plant component
    wpp = RenewableGen("Wind Power Plant").add_data_provider(wp_data_provider)

    # system
    sys = System(PowerBalanceModel()).add_node(farm).add_node(grid)

    # add components to farm
    farm.add_node(wpp).add_node(ess)

    sys.pprint()

    return sys, farm, grid, ess
