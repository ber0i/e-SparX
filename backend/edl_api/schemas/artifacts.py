from typing import List

from pydantic import BaseModel


class DataArtifact(BaseModel):
    """Schema for an artifact of type data"""

    name: str
    description: str


class ColSpec(BaseModel):
    """Schema for a column specification used in DataArtifactPandas"""

    type: str
    name: str
    required: bool


class DataArtifactPandas(BaseModel):
    """Schema for an artifact of type Pandas data"""

    name: str
    description: str
    dataset_type: str
    num_rows: int
    num_columns: int
    schema: List[ColSpec]
