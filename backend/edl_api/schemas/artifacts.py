from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class ColSpec(BaseModel):
    """Schema for a column specification used in pandas data artifacts."""

    type: str
    name: str
    required: bool


class DataArtifact(BaseModel):
    """Schema for a data artifact"""

    name: str
    description: str
    artifact_type: str
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
    input_artifact: Optional[str] = None
    output_artifact: Optional[str] = None
