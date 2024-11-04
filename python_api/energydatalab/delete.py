from ._client import auth_client


def delete_artifact(
    name: str,
):
    """
    Deletes the specified artifact.
    This also deletes all connections to and from this artifact.
    An artifact can only be deleted by its creator.


    Parameters
    ----------
    name : str
        The name of the artifact to delete.
    """

    response = auth_client.delete(
        f"/artifacts/name/{name}",
    )
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get("message", "No message provided")
        print(f"{message}")
    else:
        print("Failed to delete artifact:", response.text)


def delete_pipeline(
    name: str,
):
    """
    Deletes the specified pipeline.
    A pipeline can only be deleted by its creator and only if it is empty.


    Parameters
    ----------
    name : str
        The name of the pipeline to delete.
    """

    response = auth_client.delete(
        f"/pipelines/name/{name}",
    )
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get("message", "No message provided")
        print(f"{message}")
    else:
        print("Failed to delete pipeline:", response.text)
