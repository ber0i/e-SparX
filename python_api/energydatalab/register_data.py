import glob
import json
import os
import shutil
from typing import Optional

import mlflow
import pandas as pd
import yaml
from pydantic import HttpUrl

from ._client import auth_client


def register_data_free(
    name: str,
    description: str,
    file_type: str,
    source_url: Optional[HttpUrl] = None,
    download_url: Optional[HttpUrl] = None,
    pipeline_name: Optional[str] = None,
    source_name: Optional[str] = None,
):
    """
    Registers a free-form dataset artifact in the Energy Data Lab.
    To add an existing artifact to a pipeline, use the existing artifact name in name and define the pipeline via the pipeline_name.
    If the pipeline does not exist yet, it will be created.
    Pipeline connections are specified via the source_name parameter.
    If your artifact is a source node in the pipeline, set source_name to None (default).

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
    source_name: [Optional] str
        The name of the source artifact in the mentioned pipeline. If source node, set to None (default).
    """
    result = {
        "name": name,
        "description": description,
        "file_type": file_type,
        "artifact_type": "dataset",
        "artifact_subtype": "free-form",
        "source_url": source_url,
        "download_url": download_url,
        "pipeline_name": pipeline_name,
        "source_name": source_name,
    }

    response = auth_client.post(
        "/data-artifacts",
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
    file_type: str,
    df: pd.DataFrame,
    source_url: Optional[HttpUrl] = None,
    download_url: Optional[HttpUrl] = None,
    pipeline_name: Optional[str] = None,
    source_name: Optional[str] = None,
):
    """
    Register a pandas DataFrame as a dataset artifact in the Energy Data Lab.

    Parameters
    ----------
    name : str
        The name of the dataset.
    description : str
        The description of the dataset.
    file_type : str
        The type of the underlying files, as "CSV", "ZIP", etc.
    df : pd.DataFrame
        The pandas DataFrame to register.
    source_url: [Optional] str
        The URL on where to find the underlying file.
    download_url: [Optional] str
        The download URL of the underlying file.
    pipeline_name: [Optional] str
        The name of the ML pipeline the dataset is used in.
    source_name: [Optional] str
        The name of the source artifact in the mentioned pipeline. If source node, set to None (default).
    """

    # Reset the MLflow state
    mlflow.tracking.fluent._active_run_stack = []
    mlflow.tracking.fluent._active_experiment_id = None
    mlflow.tracking.fluent._tracking_uri = None

    os.makedirs(os.path.join("mlruns", ".trash"), exist_ok=True)
    mlruns_path = os.path.join(os.getcwd(), "mlruns")
    mlflow.set_tracking_uri(f"file:///{mlruns_path}")

    # Check if the experiment exists, if not, create a new one
    experiment_name = "Default"
    try:
        experiment_id = mlflow.create_experiment(experiment_name)
    except mlflow.exceptions.MlflowException:
        experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id

    # we only pass the first 100 rows to mlflow as otherwise, the dataset is too slow
    # the correct nrows will be extracted from df manually
    dataset = mlflow.data.from_pandas(df.head(100), name=name)

    with mlflow.start_run(experiment_id=experiment_id):
        mlflow.log_input(dataset)
    mlflow.end_run()

    datasets_path = os.path.join(mlruns_path, experiment_id, "datasets")
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
                "file_type": file_type,
                "artifact_type": "dataset",
                "artifact_subtype": "pandas.DataFrame",
                "num_rows": num_rows,
                "num_columns": num_columns,
                "data_schema": schema_data["mlflow_colspec"],
                "index_name": df.index.name,
                "index_dtype": str(df.index.dtype),
            }
            if source_url is not None:
                result["source_url"] = source_url
            if download_url is not None:
                result["download_url"] = download_url
            if pipeline_name is not None:
                result["pipeline_name"] = pipeline_name
            if source_name is not None:
                result["source_name"] = source_name
            response = auth_client.post(
                "/data-artifacts",
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

    mlflow.delete_experiment(experiment_id)
    shutil.rmtree(mlruns_path)
