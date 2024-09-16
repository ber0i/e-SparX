from pydantic import BaseModel


class ConnectionCreation(BaseModel):
    """Schema for a connection"""

    source: str
    target: str
    pipeline: str
