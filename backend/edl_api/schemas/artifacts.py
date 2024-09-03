from pydantic import BaseModel


class DataArtifact(BaseModel):
    """Schema for an artifact of type data"""

    name: str
    description: str
