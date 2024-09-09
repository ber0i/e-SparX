import urllib.parse

from fastapi import APIRouter
from pymongo.errors import DuplicateKeyError

from edl_api.documentdb import DocumentDBClient
from edl_api.schemas import DataArtifactFree, DataArtifactPandas

DataArtifactRouter = APIRouter(tags=["Data Artifact"])

db = DocumentDBClient.edl_db
collection = db.entries
collection.create_index("name", unique=True)


@DataArtifactRouter.post("/")
async def register_free_data_artifact(dataset: DataArtifactFree):
    """Register a free-form data artifact. Saves the artifact in the document database."""

    entry_data = dataset.model_dump()
    try:
        collection.insert_one(entry_data)
        return {"message": f"Artifact registered: {entry_data}"}
    except DuplicateKeyError:
        print("Error: An artifact with the same name already exists.")
        return {"error": "Artifact with this name already exists."}


@DataArtifactRouter.post("/pandas")
async def register_pandas_data_artifact(dataset: DataArtifactPandas):
    """Register a pandas.DataFrame data artifact. Saves the artifact in the document database."""

    entry_data = dataset.model_dump()
    try:
        collection.insert_one(entry_data)
        return {"message": f"Artifact registered: {entry_data}"}
    except DuplicateKeyError:
        print("Error: An artifact with the same name already exists.")
        return {"error": "Artifact with this name already exists."}


@DataArtifactRouter.get("/")
async def get_artifacts():
    """Get all artifacts"""

    entries = list(collection.find({}, {"_id": 0}))  # Omit the _id field
    return {"entries": entries}


@DataArtifactRouter.get("/{name}")
async def get_artifact_by_name(name: str):
    """Get a single data artifact by name"""

    name = urllib.parse.unquote(name)
    # Search for the artifact in the database collection
    artifact = collection.find_one({"name": name}, {"_id": 0})  # Omit the _id field

    if artifact:
        return artifact
