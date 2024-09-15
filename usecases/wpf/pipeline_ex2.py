import os

import energy_data_lab as edl
import mlflow
import pandas as pd

current_dir = os.getcwd()
file_path = os.path.join(current_dir, "usecases", "wpf", "data", "wspd2017.csv")

# current_dir = os.path.dirname(__file__)
# file_path = os.path.join(current_dir, "data", "wspd2017.csv")

df = pd.read_csv(file_path, nrows=100)
# Note: Large datasets take forever to be logged by MLflow
# (this is not my code that takes so long)
# We should think about how to handle this in the future

edl.register_data_pandas(
    name="Kelmarsh Wind Power",
    description="SCADA wind power measurements on turbine level at the Kelmarsh wind farm.",
    df=df,
    url="https://zenodo.org/records/8252025",
    pipeline_name="Wind Power Forecasting",
)

edl.register_data_free(
    name="a2",
    description="Artifact 2 in pipeline WPF.",
    pipeline_name="Wind Power Forecasting",
    parent_name="Kelmarsh Wind Power",
)
