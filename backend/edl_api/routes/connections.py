import urllib.parse
from typing import List

from fastapi import APIRouter

from edl_api.dagdb import Session
from edl_api.schemas import (
    Artifact,
    ArtifactCreation,
    Connection,
    ConnectionCreation,
    ConnectionResponse,
)

ConnectionRouter = APIRouter(tags=["Connections"])


def artifact_to_dict(artifact: Artifact) -> dict:
    return {"name": artifact.name}


def connection_to_dict(connection: Connection) -> dict:
    return {"source": artifact_to_dict(connection.source), "target": artifact_to_dict(connection.target)}


@ConnectionRouter.get("/pipeline/{pipeline_name}", response_model=List[ConnectionResponse])
async def get_connections_by_pipeline(pipeline_name: str, session: Session = Session):
    """Get all connections in a pipeline"""

    pipeline_name = urllib.parse.unquote(pipeline_name)
    # Search for the connections in the dagdb
    with session.begin() as s:
        connections = Connection.get_connections_by_pipeline(s, pipeline_name)
        connection_dicts = [connection_to_dict(connection) for connection in connections]
        return connection_dicts


@ConnectionRouter.post("/create")
async def create_connection(connection: ConnectionCreation, session: Session = Session):
    """Create a connection between two artifacts in a pipeline"""

    node_data = ArtifactCreation(name=connection.target, pipeline=connection.pipeline, parent=connection.source)

    with session.begin() as s:
        response = Artifact.create(session=s, param=node_data)

    return {"message": response}
