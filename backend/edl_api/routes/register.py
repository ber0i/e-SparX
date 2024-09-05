from fastapi import APIRouter

from edl_api.documentdb import DocumentDBClient
from edl_api.schemas import DataArtifact, DataArtifactPandas

DataArtifactRouter = APIRouter(tags=["Data Artifact"])

db = DocumentDBClient.edl_db
collection = db.entries


@DataArtifactRouter.post("/")
async def register_data_artifact(dataset: DataArtifact):
    """Register a data artifact. Saves the artifact in the document database."""

    entry_data = dataset.model_dump()
    collection.insert_one(entry_data)
    return {"message": f"Artifact registered: {entry_data}"}


@DataArtifactRouter.post("/pandas/")
async def register_pandas_data_artifact(dataset: DataArtifactPandas):
    """Register a Pandas data artifact. Saves the artifact in the document database."""

    entry_data = dataset.model_dump()
    collection.insert_one(entry_data)
    return {"message": f"Pandas artifact registered: {entry_data}"}


@DataArtifactRouter.get("/")
async def view_artifacts():
    """Get all artifacts"""

    entries = list(collection.find({}, {"_id": 0}))  # Omit the _id field
    return {"entries": entries}


@DataArtifactRouter.get("/{name}")
async def get_artifact_by_name(name: str):
    """Get a single data artifact by name"""

    # Search for the artifact in the database collection
    artifact = collection.find_one({"name": name}, {"_id": 0})  # Omit the _id field

    if artifact:
        return artifact
