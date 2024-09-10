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

DataArtifactRouter = APIRouter(tags=["Data Artifact"])

db = DocumentDBClient.artifactdb
artifact_collection = db.artifacts
artifact_collection.create_index("name", unique=True)


@DataArtifactRouter.post("/")
async def register_free_data_artifact(dataset: DataArtifactFree, session: Session = Session):
    """Register a free-form data artifact. Saves the artifact in the document database."""

    entry_data = dataset.model_dump()
    pipeline = entry_data["pipeline_name"] if entry_data["pipeline_name"] else None
    node_data = ArtifactCreation(name=entry_data["name"], pipeline=pipeline)
    try:
        # Check if an entry with the same name already exists in artifactdb
        existing_entry = artifact_collection.find_one({"name": entry_data["name"]})
        if not existing_entry:
            # Insert the new entry if the name is not found
            artifact_collection.insert_one(entry_data)
            print("Entry inserted successfully.")

        with session.begin() as s:
            response = Artifact.create(session=s, param=node_data)
        return {"message": response}
    except DuplicateKeyError:
        print("Error: An artifact with the same name already exists.")
        return {"error": "Artifact with this name already exists."}


@DataArtifactRouter.post("/pandas")
async def register_pandas_data_artifact(dataset: DataArtifactPandas):
    """Register a pandas.DataFrame data artifact. Saves the artifact in the document database."""

    entry_data = dataset.model_dump()
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
