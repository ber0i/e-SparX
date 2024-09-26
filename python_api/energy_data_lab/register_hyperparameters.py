from typing import Optional

import requests
from pydantic import HttpUrl


def register_hyperparameters(
    name: str,
    description: str,
    hyperparameters: dict,
    file_type: str,
    source_url: Optional[HttpUrl] = None,
    download_url: Optional[HttpUrl] = None,
    pipeline_name: Optional[str] = None,
    parent_name: Optional[str] = None,
):
    """
    Registers a hyperparameters artifact in the Energy Data Lab.
    To add an existing artifact to a pipeline, use the existing artifact name in name and define the pipeline via the pipeline_name.
    If the pipeline does not exist yet, it will be created.
    Pipeline connections are specified via the parent_name parameter.
    If your artifact is a source node in the pipeline, set parent_name to None (default).

    Parameters
    ----------
    name : str
        The name of the code.
    description : str
        The description of the code.
    hyperparameters : dict
        Dictionary of hyperparameters. Expected format: {"name": value, ...},
        where value can be a string, int, float, or bool.
    file_type : str
        The type of the underlying file, as "JSON", "YAML", etc.
    source_url: [Optional] str
        The URL on where to find the underlying file.
    download_url: [Optional] str
        The download URL of the underlying file.
    pipeline_name: [Optional] str
        The name of the ML pipeline the code is used in.
    parent_name: [Optional] str
        The name of the parent artifact in the mentioned pipeline. If source node, set to None (default).
    """

    hyperparameters_list = [
        {"name": name, "value": value} for name, value in hyperparameters.items()
    ]

    result = {
        "name": name,
        "description": description,
        "file_type": file_type,
        "artifact_type": "hyperparameters",
        "hyperparameters": hyperparameters_list,
        "source_url": source_url,
        "download_url": download_url,
        "pipeline_name": pipeline_name,
        "parent_name": parent_name,
    }

    response = requests.post(
        "http://localhost:8080/hyperparameters-artifacts",
        json=result,
    )
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get("message", "No message provided")
        print(f"{message}")
    else:
        print("Failed to register entry:", response.text)
