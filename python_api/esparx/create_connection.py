from ._client import auth_client


def connect(
    pipeline_name: str,
    source_name: str,
    target_name: str,
):
    """
    Connect two artifacts.

    Parameters
    ----------
    pipeline_name : str
        The name of the ML pipeline the artifact is used in.
    source_name : str
        The name of the source artifact in the mentioned pipeline.
    target_name : str
        The name of the target artifact in the mentioned pipeline.
    """
    result = {
        "source": source_name,
        "target": target_name,
        "pipeline": pipeline_name,
    }

    response = auth_client.post(
        "/connections/create",
        json=result,
    )
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get("message", "No message provided")
        print(f"{message}")
    else:
        print("Failed to connect entries:", response.text)
