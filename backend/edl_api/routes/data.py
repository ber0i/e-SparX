import urllib.parse
from typing import List

from fastapi import APIRouter
from pymongo.errors import DuplicateKeyError

from edl_api.dagdb import Session
from edl_api.documentdb import DocumentDBClient
from edl_api.schemas import (
    Artifact,
    ArtifactCreation,
    ArtifactResponse,
    DataArtifactFree,
    DataArtifactPandas,
)

DataArtifactRouter = APIRouter(tags=["Data Artifacts"])

db = DocumentDBClient.artifactdb
artifact_collection = db.artifacts
artifact_collection.create_index("name", unique=True)


@DataArtifactRouter.post("/")
async def register_free_data_artifact(dataset: DataArtifactFree, session: Session = Session):
    """Register a free-form data artifact."""

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
        if entry_data["url"]:
            entry_data["url"] = str(entry_data["url"])
        # remove pipeline-related logic
        entry_data.pop("pipeline_name", None)
        entry_data.pop("parent_name", None)
        artifact_collection.insert_one(entry_data)
        print("New artifact inserted successfully in artifactdb.")
    else:
        print("Artifact already exists in artifactdb.")

    # Handle dagdb operations (logic is inside the create method)
    node_data = ArtifactCreation(name=entry_data["name"], pipeline=pipeline, parent=parent)
    with session.begin() as s:
        response = Artifact.create(session=s, param=node_data)

    return {"message": response}


@DataArtifactRouter.post("/pandas")
async def register_pandas_data_artifact(dataset: DataArtifactPandas):
    """Register a pandas.DataFrame data artifact."""

    entry_data = dataset.model_dump()
    if entry_data["url"]:
        entry_data["url"] = str(entry_data["url"])
    try:
        artifact_collection.insert_one(entry_data)
        return {"message": f"Artifact registered: {entry_data}"}
    except DuplicateKeyError:
        print("Error: An artifact with the same name already exists.")
        return {"error": "Artifact with this name already exists."}


@DataArtifactRouter.get("/")
async def get_artifacts():
    """Get all artifacts"""

    entries = list(artifact_collection.find({}, {"_id": 0}))  # Omit the _id field
    return {"entries": entries}


@DataArtifactRouter.get("/{name}")
async def get_artifact_by_name(name: str):
    """Get a single data artifact by name"""

    name = urllib.parse.unquote(name)
    # Search for the artifact in the database collection
    artifact = artifact_collection.find_one({"name": name}, {"_id": 0})  # Omit the _id field

    if artifact:
        return artifact


def artifact_to_dict(artifact: Artifact) -> dict:
    return {"id": artifact.id, "name": artifact.name}


@DataArtifactRouter.get("/pipeline/{pipeline_name}", response_model=List[ArtifactResponse])
async def get_artifacts_by_pipeline(pipeline_name: str, session: Session = Session):
    """Get all artifacts in a pipeline"""

    pipeline_name = urllib.parse.unquote(pipeline_name)
    # Search for the artifacts in the database collection
    with session.begin() as s:
        artifacts = Artifact.get_artifacts_by_pipeline(s, pipeline_name)
        artifacts_dicts = [artifact_to_dict(artifact) for artifact in artifacts]
        return [ArtifactResponse.model_validate(artifact_dict) for artifact_dict in artifacts_dicts]
