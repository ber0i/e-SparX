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
    dataset_type: str
    created_at: datetime = datetime.now()
    source_url: Optional[HttpUrl] = None
    download_url: Optional[HttpUrl] = None
    pipeline_name: Optional[str] = None
    parent_name: Optional[str] = None
    num_rows: Optional[int] = None
    num_columns: Optional[int] = None
    data_schema: Optional[List[ColSpec]] = None
