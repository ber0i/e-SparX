from typing import Optional

from pydantic import HttpUrl

from ._client import auth_client


def register_code(
    name: str,
    description: str,
    file_type: str,
    source_url: Optional[HttpUrl] = None,
    download_url: Optional[HttpUrl] = None,
    pipeline_name: Optional[str] = None,
    source_name: Optional[str] = None,
):
    """
    Registers a code artifact in the Energy Data Lab.
    To add an existing artifact to a pipeline, use the existing artifact name in name and define the pipeline via the pipeline_name.
    If the pipeline does not exist yet, it will be created.
    Pipeline connections are specified via the source_name parameter.
    If your artifact is a source node in the pipeline, set source_name to None (default).

    Parameters
    ----------
    name : str
        The name of the code.
    description : str
        The description of the code.
    file_type : str
        The type of the underlying file, as "PY", "IPYNB", etc.
    source_url: [Optional] str
        The URL on where to find the underlying file.
    download_url: [Optional] str
        The download URL of the underlying file.
    pipeline_name: [Optional] str
        The name of the ML pipeline the code is used in.
    source_name: [Optional] str
        The name of the source artifact in the mentioned pipeline. If source node, set to None (default).
    """
    result = {
        "name": name,
        "description": description,
        "file_type": file_type,
        "artifact_type": "code",
        "source_url": source_url,
        "download_url": download_url,
        "pipeline_name": pipeline_name,
        "source_name": source_name,
    }

    response = auth_client.post(
        "/code-artifacts",
        json=result,
    )
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get("message", "No message provided")
        print(f"{message}")
    else:
        print("Failed to register entry:", response.text)
