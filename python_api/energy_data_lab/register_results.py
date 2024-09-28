from typing import Optional

import requests


def register_results(
    name: str,
    description: str,
    results: dict,
    pipeline_name: Optional[str] = None,
    parent_name: Optional[str] = None,
):
    """
    Registers a results artifact in the Energy Data Lab.
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
    results : dict
        Dictionary of metrics and their value. Expected format: {"metric_name": value, ...},
        where value must be a float.
    pipeline_name: [Optional] str
        The name of the ML pipeline the code is used in.
    parent_name: [Optional] str
        The name of the parent artifact in the mentioned pipeline. If source node, set to None (default).
    """

    results_list = [
        {"metric": metric, "value": value} for metric, value in results.items()
    ]

    result = {
        "name": name,
        "description": description,
        "artifact_type": "results",
        "results": results_list,
        "pipeline_name": pipeline_name,
        "parent_name": parent_name,
    }

    response = requests.post(
        "http://localhost:8080/results-artifacts",
        json=result,
    )
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get("message", "No message provided")
        print(f"{message}")
    else:
        print("Failed to register entry:", response.text)
