from fastapi import APIRouter

from edl_api.documentdb import DocumentDBClient
from edl_api.schemas import DataArtifact

RegisterRouter = APIRouter(tags=["Register"])

db = DocumentDBClient.edl_db
collection = db.entries


@RegisterRouter.post("/")
async def register_artifact(dataset: DataArtifact):
    """Register an artifact. Saves the artifact in the document database."""

    entry_data = dataset.model_dump()
    collection.insert_one(entry_data)
    return {"message": f"Artifact registered: {entry_data}"}


@RegisterRouter.get("/")
async def view_artifacts():
    """Get all artifacts"""

    entries = list(collection.find({}, {"_id": 0}))  # Omit the _id field
    return {"entries": entries}
