from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class ColSpec(BaseModel):
    """Schema for a column specification used in pandas data artifacts."""

    type: str
    name: str
    required: bool


class TensorSpec(BaseModel):
    """Schema for a tensor specification used in PyTorch model artifacts."""

    dtype: str
    shape: List[int]


class PyTorchFormat(BaseModel):
    """Schema for an input/output format used in PyTorch model artifacts."""

    type: str
    tensor_spec: TensorSpec


class Hyperparameter(BaseModel):
    """Schema for a hyperparameter used in hyperparameters artifacts."""

    name: str
    value: float | int | str | bool


class Result(BaseModel):
    """Schema for a result used in results artifacts."""

    metric: str
    value: float


class DataArtifact(BaseModel):
    """Schema for a data artifact"""

    name: str
    description: str
    artifact_type: str
    artifact_subtype: str
    file_type: str
    created_at: datetime = datetime.now()
    source_url: Optional[HttpUrl] = None
    download_url: Optional[HttpUrl] = None
    pipeline_name: Optional[str] = None
    parent_name: Optional[str] = None
    num_rows: Optional[int] = None
    num_columns: Optional[int] = None
    data_schema: Optional[List[ColSpec]] = None
    index_name: Optional[str] = None
    index_dtype: Optional[str] = None


class CodeArtifact(BaseModel):
    """Schema for a code artifact"""

    name: str
    description: str
    artifact_type: str
    file_type: str
    created_at: datetime = datetime.now()
    source_url: Optional[HttpUrl] = None
    download_url: Optional[HttpUrl] = None
    pipeline_name: Optional[str] = None
    parent_name: Optional[str] = None


class ModelArtifact(BaseModel):
    """Schema for a model artifact"""

    name: str
    description: str
    artifact_type: str
    flavor: str
    file_type: str
    created_at: datetime = datetime.now()
    source_url: Optional[HttpUrl] = None
    download_url: Optional[HttpUrl] = None
    pipeline_name: Optional[str] = None
    parent_name: Optional[str] = None
    dependencies: Optional[List[str]] = None
    input_format: Optional[List[PyTorchFormat]] = None
    output_format: Optional[List[PyTorchFormat]] = None


class HyperparametersArtifact(BaseModel):
    """Schema for a hyperparameters artifact"""

    name: str
    description: str
    artifact_type: str
    file_type: str
    created_at: datetime = datetime.now()
    source_url: Optional[HttpUrl] = None
    download_url: Optional[HttpUrl] = None
    hyperparameters: List[Hyperparameter]
    pipeline_name: Optional[str] = None
    parent_name: Optional[str] = None


class ParametersArtifact(BaseModel):
    """Schema for a parameters artifact"""

    name: str
    description: str
    artifact_type: str
    file_type: str
    created_at: datetime = datetime.now()
    source_url: Optional[HttpUrl] = None
    download_url: Optional[HttpUrl] = None
    pipeline_name: Optional[str] = None
    parent_name: Optional[str] = None


class ResultsArtifact(BaseModel):
    """Schema for a results artifact"""

    name: str
    description: str
    artifact_type: str
    file_type: str
    results: List[Result]
    created_at: datetime = datetime.now()
    pipeline_name: Optional[str] = None
    parent_name: Optional[str] = None
