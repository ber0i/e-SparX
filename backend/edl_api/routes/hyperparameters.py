from fastapi import APIRouter

from edl_api.dagdb import Session
from edl_api.documentdb import DocumentDBClient
from edl_api.schemas import Artifact, ArtifactCreation, HyperparametersArtifact

HyperparametersArtifactRouter = APIRouter(tags=["Hyperparameters Artifacts"])

db = DocumentDBClient.artifactdb
artifact_collection = db.artifacts
artifact_collection.create_index("name", unique=True)


@HyperparametersArtifactRouter.post("/")
async def register_hyperparameters_artifact(hyperparameters: HyperparametersArtifact, session: Session = Session):
    """Register a hyperparameters artifact."""

    entry_data = hyperparameters.model_dump()
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
    with session.begin() as s:
        response = Artifact.create(session=s, param=node_data)

    return {"message": response}
