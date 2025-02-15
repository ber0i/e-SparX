import glob
import json
import os
import shutil
from typing import Optional

import mlflow
import torch
import yaml
from mlflow.models import infer_signature
from pydantic import HttpUrl
from torch import nn

from ._client import auth_client


def register_model_pytorch(
    name: str,
    description: str,
    file_type: str,
    model: nn.Module,
    input_example: torch.Tensor,
    source_url: Optional[HttpUrl] = None,
    download_url: Optional[HttpUrl] = None,
    pipeline_name: Optional[str] = None,
    source_name: Optional[str] = None,
):
    """
    Register a PyToroch nn.Module as model in e-SparX.

    Parameters
    ----------
    name : str
        The name of the dataset.
    description : str
        The description of the dataset.
    file_type : str
        The type of the underlying file, as "PY", "IPYNB", etc.
    model: nn.Module
        The PyTorch model to register.
    input_example: torch.Tensor
        An example input tensor to infer the in and output format of the model.
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

    with mlflow.start_run(experiment_id=experiment_id):
        signature = infer_signature(
            input_example.numpy(), model(input_example).detach().numpy()
        )
        mlflow.pytorch.log_model(model, "model", signature=signature)
    mlflow.end_run()

    model_path_pattern = os.path.join(
        mlruns_path, experiment_id, "*", "artifacts", "model"
    )
    model_path = glob.glob(model_path_pattern)[0]
    mlmodel_path = os.path.join(model_path, "MLmodel")

    with open(mlmodel_path, "r") as file:
        content = file.read()

    # parse content
    parsed_data = yaml.safe_load(content)

    # extract the 'signature' part
    signature_extracted = parsed_data.get("signature")
    input_format = json.loads(signature_extracted["inputs"])
    output_format = json.loads(signature_extracted["outputs"])

    # exchange the key "tensor-spec" with "tensor_spec"
    for item in input_format:
        item["tensor_spec"] = item.pop("tensor-spec")
    for item in output_format:
        item["tensor_spec"] = item.pop("tensor-spec")

    requirements_path = os.path.join(model_path, "requirements.txt")

    with open(requirements_path, "r") as file:
        requirements = [line.strip() for line in file.readlines()]

    # Construct the desired JSON structure
    result = {
        "name": name,
        "description": description,
        "flavor": "PyTorch",
        "file_type": file_type,
        "dependencies": requirements,
        "input_format": input_format,
        "output_format": output_format,
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
        "/register/model",
        json=result,
    )
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get("message", "No message provided")
        print(f"{message}")
    else:
        print("Failed to register entry:", response.text)

    mlflow.delete_experiment(experiment_id)
    shutil.rmtree(mlruns_path)


def register_model_free(
    name: str,
    description: str,
    file_type: str,
    flavor: Optional[str] = None,
    source_url: Optional[HttpUrl] = None,
    download_url: Optional[HttpUrl] = None,
    pipeline_name: Optional[str] = None,
    source_name: Optional[str] = None,
):
    """
    Register a PyToroch nn.Module as model in e-SparX.

    Parameters
    ----------
    name : str
        The name of the dataset.
    description : str
        The description of the dataset.
    file_type : str
        The type of the underlying file, as "PY", "IPYNB", etc.
    flavor: [Optional] str
        The flavor of the model, e.g., "keras".
    source_url: [Optional] str
        The URL on where to find the underlying file.
    download_url: [Optional] str
        The download URL of the underlying file.
    pipeline_name: [Optional] str
        The name of the ML pipeline the dataset is used in.
    source_name: [Optional] str
        The name of the source artifact in the mentioned pipeline. If source node, set to None (default).
    """

    # Construct the desired JSON structure
    result = {
        "name": name,
        "description": description,
        "file_type": file_type,
    }
    if flavor is not None:
        result["flavor"] = flavor
    else:
        result["flavor"] = "not available"
    if source_url is not None:
        result["source_url"] = source_url
    if download_url is not None:
        result["download_url"] = download_url
    if pipeline_name is not None:
        result["pipeline_name"] = pipeline_name
    if source_name is not None:
        result["source_name"] = source_name
    response = auth_client.post(
        "/register/model",
        json=result,
    )
    if response.status_code == 200:
        response_json = response.json()
        message = response_json.get("message", "No message provided")
        print(f"{message}")
    else:
        print("Failed to register entry:", response.text)
