"""
Unzips the raw SCADA data from Penmanshiel wind farm,
extracts the relevant variables
and saves it to a CSV file.
"""

import os
import zipfile

import esparx
import pandas as pd

raw_data_path = "usecases/wpf/alice/data/raw"
unpack_path = os.path.join(raw_data_path, "unpacked")
processed_data_path = "usecases/wpf/alice/data/processed"

# register raw data in e-SparX
print(">>>>>>>>>>Registering raw data in e-SparX<<<<<<<<<<")
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

# check whether processed data already exists
if os.path.exists(os.path.join(processed_data_path, "Penmanshiel_SCADA_2022.csv")):
    # if yes, load data
    print("Data already processed. Loading as pandas DataFrame.")
    df = pd.read_csv(
        os.path.join(processed_data_path, "Penmanshiel_SCADA_2022.csv"), index_col=0
    )
    print("Done.")
else:
    # if not, continue with preprocessing
    print("Data not yet processed. Continuing with preprocessing:")

    # unpack SCADA ZIP files
    print("Unpacking SCADA ZIP files.")
    zip_path = os.path.join(raw_data_path, "Penmanshiel_SCADA_2022_WT01-10_4462.zip")
    zip_ref = zipfile.ZipFile(zip_path, "r")
    zip_ref.extractall(unpack_path)
    zip_ref.close()
    zip_path = os.path.join(raw_data_path, "Penmanshiel_SCADA_2022_WT11-15_4463.zip")
    zip_ref = zipfile.ZipFile(zip_path, "r")
    zip_ref.extractall(unpack_path)
    zip_ref.close()
    print("Done.")

    # loop over all file names in raw_data_path/unpacked starting with "Turbine"
    # and write the CSV file to a pandas DataFrame
    print("Extracting relevant data from SCADA files.")
    df_list = []
    turbine_ids = [i for i in range(1, 16) if i != 3]  # turbine 3 is missing in data
    mycolumns = [
        "# Date and time",
        "Wind speed (m/s)",
        "Wind direction (°)",
        "Nacelle position (°)",
        "Vane position 1+2 (°)",
        "Power (kW)",
        "Potential power learned PC (kW)",
    ]
    idx = 0
    for file_name in os.listdir(unpack_path):
        if file_name.startswith("Turbine"):
            df = pd.read_csv(
                os.path.join(unpack_path, file_name),
                skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8],
                index_col=0,
                parse_dates=True,
                usecols=mycolumns,
            )
            df["turbine"] = f"T{turbine_ids[idx]:02d}"
            df_list.append(df)
            idx += 1
    print("Done.")

    # concatenate the SCADA dfs
    print("Saving data to one CSV file.")
    df = pd.concat(df_list)  # Concatenate the SCADA dfs
    df["timestamp"] = df.index.astype(str)
    df["timestamp_turbine"] = df.index.astype(str) + " " + df["turbine"]
    # set new index but keep old index as column
    df.set_index("timestamp_turbine", inplace=True)
    df.to_csv(os.path.join(processed_data_path, "Penmanshiel_SCADA_2022.csv"))
    print("Done.")

# register processed data in e-SparX
print(">>>>>>>>>>Registering processed data in e-SparX<<<<<<<<<<")
esparx.register_dataset_pandas(
    name="Penmanshiel SCADA 2022",
    description="Processed Penmanshiel SCADA data from 2022, all turbines.",
    file_type="CSV",
    df=df,
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
)


# register this script in e-SparX
print(">>>>>>>>>>Registering this preprocessing script in e-SparX<<<<<<<<<<")
esparx.register_code(
    name="Extract Penmanshiel Data",
    description="Extract relevant variables from raw SCADA data from Penmanshiel wind farm and save it to one CSV file.",
    file_type="PY",
    source_url="https://gitlab.lrz.de/energy-management-technologies-public/e-sparx/-/blob/main/usecases/wpf/alice/src/b_preprocess_power_data.py",
    download_url="https://gitlab.lrz.de/energy-management-technologies-public/e-sparx/-/raw/main/usecases/wpf/alice/src/b_preprocess_power_data.py?inline=false",
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Penmanshiel SCADA 2022 WT01-10",
)

# set remaining pipeline connections in e-SparX
print(">>>>>>>>>>Setting additional pipeline connections in e-SparX<<<<<<<<<<")
esparx.connect(
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Penmanshiel SCADA 2022 WT11-15",
    target_name="Extract Penmanshiel Data",
)
esparx.connect(
    pipeline_name="Wind Power Forecasting - MLP and LSTM",
    source_name="Extract Penmanshiel Data",
    target_name="Penmanshiel SCADA 2022",
)
print("Script finished.")
