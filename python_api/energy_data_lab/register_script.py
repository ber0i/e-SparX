from typing import Optional

import requests
from pydantic import HttpUrl


def register_script(
    name: str,
    description: str,
    file_type: str,
    source_url: Optional[HttpUrl] = None,
    download_url: Optional[HttpUrl] = None,
    pipeline_name: Optional[str] = None,
    parent_name: Optional[str] = None,
):
    """
    Registers a code script artifact in the Energy Data Lab.
    To add an existing artifact to a pipeline, use the existing artifact name in name and define the pipeline via the pipeline_name.
    If the pipeline does not exist yet, it will be created.
    Pipeline connections are specified via the parent_name parameter.
    If your artifact is a source node in the pipeline, set parent_name to None (default).

    Parameters
    ----------
    name : str
        The name of the script.
    description : str
        The description of the script.
    file_type : str
        The type of the underlying file, as "PY", "IPYNB", etc.
    source_url: [Optional] str
        The URL on where to find the underlying file.
    download_url: [Optional] str
        The download URL of the underlying file.
    pipeline_name: [Optional] str
        The name of the ML pipeline the script is used in.
    parent_name: [Optional] str
        The name of the parent artifact in the mentioned pipeline. If source node, set to None (default).
    """
    result = {
        "name": name,
        "description": description,
        "file_type": file_type,
        "artifact_type": "script",
        "source_url": source_url,
        "download_url": download_url,
        "pipeline_name": pipeline_name,
        "parent_name": parent_name,
    }

    response = requests.post(
        "http://localhost:8080/script-artifacts",
        json=result,
    )
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get("message", "No message provided")
        print(f"{message}")
    else:
        print("Failed to register entry:", response.text)
