import requests


def connect(
    pipeline_name: str,
    parent_name: str,
    target_name: str,
):
    """
    Connect two artifacts in the Energy Data Lab.

    Parameters
    ----------
    pipeline_name : str
        The name of the ML pipeline the artifact is used in.
    parent_name : str
        The name of the parent artifact in the mentioned pipeline.
    target_name : str
        The name of the target artifact in the mentioned pipeline.
    """
    result = {
        "source": parent_name,
        "target": target_name,
        "pipeline": pipeline_name,
    }

    response = requests.post(
        "http://localhost:8080/connections/create",
        json=result,
    )
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get("message", "No message provided")
        print(f"{message}")
    else:
        print("Failed to connect entries:", response.text)
