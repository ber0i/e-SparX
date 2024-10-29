import urllib.parse
from typing import List

from fastapi import APIRouter, HTTPException, status

from edl_api.dagdb import Session
from edl_api.dependencies.auth import IdentifiedUser
from edl_api.documentdb import DocumentDBClient
from edl_api.schemas import Artifact, ArtifactCreation, ArtifactResponse, DataArtifact

DataArtifactRouter = APIRouter(tags=["Data Artifacts"])

db = DocumentDBClient.artifactdb
artifact_collection = db.artifacts
artifact_collection.create_index("name", unique=True)


@DataArtifactRouter.post("/")
async def register_data_artifact(dataset: DataArtifact, session: Session, user: IdentifiedUser):
    """Register a data artifact. Currently supported: Free-form and pd.DataFrame data artifacts."""

    entry_data = dataset.model_dump()
    pipeline = entry_data["pipeline_name"] if entry_data["pipeline_name"] else None
    parent = entry_data["parent_name"] if entry_data["parent_name"] else None

    if parent and not pipeline:
        return {"error": "Parent artifact specified without pipeline."}
    if parent:
        parent_entry = artifact_collection.find_one({"name": entry_data["parent_name"]})
        if not parent_entry:
            return {"error": "Parent artifact does not exist. Create the parent artifact first."}

    # If artifact does not exist in artifactdb, insert it
    existing_entry = artifact_collection.find_one({"name": entry_data["name"]})
    if not existing_entry:
        if entry_data["source_url"]:
            entry_data["source_url"] = str(entry_data["source_url"])
        if entry_data["download_url"]:
            entry_data["download_url"] = str(entry_data["download_url"])
        # remove pipeline-related logic
        entry_data.pop("pipeline_name", None)
        entry_data.pop("parent_name", None)
        artifact_collection.insert_one(entry_data)
        print("New artifact inserted successfully in artifactdb.")
    else:
        print("Artifact already exists in artifactdb.")

    # Handle dagdb operations (logic is inside the create method)
    node_data = ArtifactCreation(
        name=entry_data["name"], artifact_type=entry_data["artifact_type"], pipeline=pipeline, parent=parent
    )

    try:
        with session.begin() as s:
            response = Artifact.create(session=s, param=node_data, user_id=user.id)
    except PermissionError as err:
        return HTTPException(status.HTTP_401_UNAUTHORIZED, err)

    return {"message": response}


@DataArtifactRouter.get("/")
async def get_artifacts():
    """Get all artifacts"""

    entries = list(artifact_collection.find({}, {"_id": 0}))  # Omit the _id field
    return {"entries": entries}


def artifact_to_dict(artifact: Artifact) -> dict:
    return {
        "id": artifact.id,
        "name": artifact.name,
        "artifact_type": artifact.artifact_type,
    }


@DataArtifactRouter.get("/global", response_model=List[ArtifactResponse])
async def get_artifacts_for_global_view(session: Session = Session):
    """Get all artifacts from the DAG DB for global view"""

    with session.begin() as s:
        artifacts = Artifact.get_all_artifacts(s)
        artifacts_dicts = [artifact_to_dict(artifact) for artifact in artifacts]
        return [ArtifactResponse.model_validate(artifact_dict) for artifact_dict in artifacts_dicts]


@DataArtifactRouter.get("/{name}")
async def get_artifact_by_name(name: str):
    """Get a single data artifact by name"""

    name = urllib.parse.unquote(name)
    # Search for the artifact in the database collection
    artifact = artifact_collection.find_one({"name": name}, {"_id": 0})  # Omit the _id field

    if not artifact:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Artifact not found")
    
    return artifact


@DataArtifactRouter.get("/pipeline/{pipeline_name}", response_model=List[ArtifactResponse])
async def get_artifacts_by_pipeline(pipeline_name: str, session: Session = Session):
    """Get all artifacts in a pipeline"""

    pipeline_name = urllib.parse.unquote(pipeline_name)
    # Search for the artifacts in the database collection
    with session.begin() as s:
        artifacts = Artifact.get_artifacts_by_pipeline(s, pipeline_name)
        artifacts_dicts = [artifact_to_dict(artifact) for artifact in artifacts]
        return [ArtifactResponse.model_validate(artifact_dict) for artifact_dict in artifacts_dicts]
