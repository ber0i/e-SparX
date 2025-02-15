import urllib.parse
from typing import List

from fastapi import APIRouter, HTTPException, status

from esparx_api.dagdb import Session
from esparx_api.dependencies.auth import IdentifiedUser
from esparx_api.documentdb import DocumentDBClient
from esparx_api.schemas import Artifact, ArtifactResponse

ArtifactRouter = APIRouter(tags=["Artifacts"])

db = DocumentDBClient.artifactdb
artifact_collection = db.artifacts
artifact_collection.create_index("name", unique=True)


@ArtifactRouter.get("/")
async def get_artifacts():
    """Get all artifacts from the DocumentDB"""

    entries = list(artifact_collection.find({}, {"_id": 0}))  # Omit the _id field
    return {"entries": entries}


def artifact_to_dict(artifact: Artifact) -> dict:
    return {
        "id": artifact.id,
        "name": artifact.name,
        "artifact_type": artifact.artifact_type,
    }


@ArtifactRouter.get("/global", response_model=List[ArtifactResponse])
async def get_artifacts_for_global_view(session: Session):
    """Get all artifacts from the DAG DB for global view"""

    with session.begin() as s:
        artifacts = Artifact.get_all_artifacts(s)
        artifacts_dicts = [artifact_to_dict(artifact) for artifact in artifacts]
        return [ArtifactResponse.model_validate(artifact_dict) for artifact_dict in artifacts_dicts]


@ArtifactRouter.get("/pipeline/{pipeline_name:path}", response_model=List[ArtifactResponse])
async def get_artifacts_by_pipeline(pipeline_name: str, session: Session):
    """Get all artifacts in a pipeline"""

    pipeline_name = urllib.parse.unquote(pipeline_name)
    # Search for the artifacts in the database collection
    with session.begin() as s:
        artifacts = Artifact.get_artifacts_by_pipeline(s, pipeline_name)
        artifacts_dicts = [artifact_to_dict(artifact) for artifact in artifacts]
        return [ArtifactResponse.model_validate(artifact_dict) for artifact_dict in artifacts_dicts]


@ArtifactRouter.get("/neighbors/{name:path}", response_model=List[ArtifactResponse])
async def get_neighbors(name: str, session: Session):
    """Get all neighbors (in any pipeline) of an artifact by artifact name"""

    name = urllib.parse.unquote(name)
    with session.begin() as s:
        # get pipelines of the artifact
        artifact = Artifact.get_artifact_by_name(s, name)
        connections_as_source = artifact.connections_as_source
        connections_as_target = artifact.connections_as_target
        # create list of all artifacts in the connection lists
        target_neighbors = [connection.target for connection in connections_as_source]
        source_neighbors = [connection.source for connection in connections_as_target]
        neighbors = target_neighbors + source_neighbors
        neighbors_dicts = [artifact_to_dict(neighbor) for neighbor in neighbors]
        neighbors_response = [ArtifactResponse.model_validate(neighbor_dict) for neighbor_dict in neighbors_dicts]
        # return {"neighbors": neighbors_response}
        return neighbors_response


@ArtifactRouter.get("/name/{name:path}")
async def get_artifact_by_name(name: str):
    """Get a single artifact by name"""

    name = urllib.parse.unquote(name)
    # Search for the artifact in the database collection
    artifact = artifact_collection.find_one({"name": name}, {"_id": 0})  # Omit the _id field

    if not artifact:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Artifact not found")

    return artifact


@ArtifactRouter.delete("/name/{name:path}")
async def remove_artifact_by_name(name: str, session: Session, user: IdentifiedUser):
    """Remove a single artifact by name"""

    name = urllib.parse.unquote(name)
    artifact_collection.delete_one({"name": name})

    try:
        with session.begin() as s:
            response = Artifact.remove(s, name, user.id)
    except ValueError as err:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(err))
    except PermissionError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(err))

    return {"message": response}
