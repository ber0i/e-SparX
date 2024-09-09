from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class DataArtifactFree(BaseModel):
    """Schema for a free-form data artifact"""

    name: str
    description: str
    dataset_type: str
    created_at: datetime = datetime.now()
    url: Optional[HttpUrl] = None


class ColSpec(BaseModel):
    """Schema for a column specification used in DataArtifactPandas"""

    type: str
    name: str
    required: bool


class DataArtifactPandas(BaseModel):
    """Schema for a pandas.DataFrame data artifact"""

    name: str
    description: str
    dataset_type: str
    created_at: datetime = datetime.now()
    url: Optional[HttpUrl] = None
    num_rows: int
    num_columns: int
    schema: List[ColSpec]
