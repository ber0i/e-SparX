import glob
import json
import os
import shutil
from typing import Optional

import mlflow
import pandas as pd
import requests
import yaml
from pydantic import HttpUrl


def register_data_free(name: str, description: str, url: Optional[HttpUrl] = None):
    """
    Register a free-form dataset artifact in the Energy Data Lab.

    Parameters
    ----------
    name : str
        The name of the dataset.
    description : str
        The description of the dataset.
    url: [Optional] str
        The URL on where to access the underlying file.
    """
    if url is None:
        result = {"name": name, "description": description, "dataset_type": "free-form"}
    else:
        result = {
            "name": name,
            "description": description,
            "dataset_type": "free-form",
            "url": url,
        }

    response = requests.post(
        "http://localhost:8080/data-artifact",
        json=result,
    )
    if response.status_code == 200:
        print("Entry registered successfully", response.json())
    else:
        print("Failed to register entry:", response.text)


def register_data_pandas(
    name: str, description: str, df: pd.DataFrame, url: Optional[HttpUrl] = None
):
    """
    Register a pandas DataFrame as a dataset artifact in the Energy Data Lab.

    Parameters
    ----------
    name : str
        The name of the dataset.
    description : str
        The description of the dataset.
    df : pd.DataFrame
        The pandas DataFrame to register.
    url: [Optional] str
        The URL on where to access the underlying file.
    """
    dataset = mlflow.data.from_pandas(df, name=name)
    mlflow.log_input(dataset)
    mlruns_path = mlflow.get_tracking_uri().replace("file:///", "")
    datasets_path = os.path.join(mlruns_path, "0", "datasets")
    datasets_dir = glob.glob(os.path.join(datasets_path, "*"))[0]

    if datasets_dir:  # Check if the directory was found
        meta_yaml_path = os.path.join(datasets_dir, "meta.yaml")

        # Ensure the meta.yaml file exists before trying to read it
        if os.path.exists(meta_yaml_path):
            with open(meta_yaml_path, "r") as yaml_file:
                meta_data = yaml.safe_load(yaml_file)

            # Extract 'profile' and 'schema' fields and parse them as JSON
            profile_data = json.loads(meta_data.get("profile", "{}"))
            schema_data = json.loads(meta_data.get("schema", "{}"))

            # Extract number of rows and columns
            num_rows = profile_data["num_rows"]
            num_columns = len(schema_data["mlflow_colspec"])

            # Construct the desired JSON structure
            result = {
                "name": name,
                "description": description,
                "dataset_type": "pandas.DataFrame",
                "num_rows": num_rows,
                "num_columns": num_columns,
                "schema": schema_data["mlflow_colspec"],
            }
            if url is not None:
                result["url"] = url
            response = requests.post(
                "http://localhost:8080/data-artifact/pandas/",
                json=result,
            )
            if response.status_code == 200:
                print("Entry registered successfully", response.json())
            else:
                print("Failed to register entry:", response.text)
        else:
            print(f"File {meta_yaml_path} does not exist.")
    else:
        print(f"No directories found in {datasets_path}.")

    shutil.rmtree(os.path.join(mlruns_path))
