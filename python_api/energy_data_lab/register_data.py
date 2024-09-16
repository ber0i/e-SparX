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


def register_data_free(
    name: str,
    description: str,
    file_type: str,
    source_url: Optional[HttpUrl] = None,
    download_url: Optional[HttpUrl] = None,
    pipeline_name: Optional[str] = None,
    parent_name: Optional[str] = None,
):
    """
    Registers a free-form dataset artifact in the Energy Data Lab.
    To add an existing artifact to a pipeline, use the existing artifact name in name and define the pipeline via the pipeline_name.
    If the pipeline does not exist yet, it will be created.
    Pipeline connections are specified via the parent_name parameter.
    If your artifact is a source node in the pipeline, set parent_name to None (default).

    Parameters
    ----------
    name : str
        The name of the dataset.
    description : str
        The description of the dataset.
    file_type : str
        The type of the underlying file, as "CSV", "ZIP", etc.
    source_url: [Optional] str
        The URL on where to find the underlying file.
    download_url: [Optional] str
        The download URL of the underlying file.
    pipeline_name: [Optional] str
        The name of the ML pipeline the dataset is used in.
    parent_name: [Optional] str
        The name of the parent artifact in the mentioned pipeline. If source node, set to None (default).
    """
    result = {
        "name": name,
        "description": description,
        "file_type": file_type,
        "artifact_type": "dataset",
        "source_url": source_url,
        "download_url": download_url,
        "pipeline_name": pipeline_name,
        "parent_name": parent_name,
    }

    response = requests.post(
        "http://localhost:8080/data-artifacts",
        json=result,
    )
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get("message", "No message provided")
        print(f"{message}")
    else:
        print("Failed to register entry:", response.text)


def register_data_pandas(
    name: str,
    description: str,
    df: pd.DataFrame,
    source_url: Optional[HttpUrl] = None,
    download_url: Optional[HttpUrl] = None,
    pipeline_name: Optional[str] = None,
    parent_name: Optional[str] = None,
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
    source_url: [Optional] str
        The URL on where to find the underlying file.
    download_url: [Optional] str
        The download URL of the underlying file.
    pipeline_name: [Optional] str
        The name of the ML pipeline the dataset is used in.
    parent_name: [Optional] str
        The name of the parent artifact in the mentioned pipeline. If source node, set to None (default).
    """

    # we only pass the first 100 rows to mlflow as otherwise, the dataset is too slow
    # the correct nrows will be extracted from df manually
    dataset = mlflow.data.from_pandas(df.head(100), name=name)
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

            # Extract 'schema' field and parse it as JSON
            schema_data = json.loads(meta_data.get("schema", "{}"))

            # Extract number of rows and columns
            num_rows = len(df)
            num_columns = len(schema_data["mlflow_colspec"])

            # Construct the desired JSON structure
            result = {
                "name": name,
                "description": description,
                "artifact_type": "dataset",
                "file_type": "pandas.DataFrame",
                "num_rows": num_rows,
                "num_columns": num_columns,
                "data_schema": schema_data["mlflow_colspec"],
            }
            if source_url is not None:
                result["source_url"] = source_url
            if download_url is not None:
                result["download_url"] = download_url
            if pipeline_name is not None:
                result["pipeline_name"] = pipeline_name
            if parent_name is not None:
                result["parent_name"] = parent_name
            response = requests.post(
                "http://localhost:8080/data-artifacts",
                json=result,
            )
            if response.status_code == 200:
                response_json = response.json()
                message = response_json.get("message", "No message provided")
                print(f"{message}")
            else:
                print("Failed to register entry:", response.text)
        else:
            print(f"File {meta_yaml_path} does not exist.")
    else:
        print(f"No directories found in {datasets_path}.")

    shutil.rmtree(os.path.join(mlruns_path))
