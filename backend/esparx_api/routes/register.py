from fastapi import APIRouter, HTTPException, status

from esparx_api.dagdb import Session
from esparx_api.dependencies import IdentifiedUser
from esparx_api.documentdb import DocumentDBClient
from esparx_api.schemas import Artifact, ArtifactCreation, CodeArtifact
from esparx_api.schemas.artifacts import (
    DatasetArtifact,
    HyperparametersArtifact,
    ModelArtifact,
    ParametersArtifact,
    ResultsArtifact,
)

ArtifactRegisterRouter = APIRouter(tags=["Artifacts"])

db = DocumentDBClient.artifactdb
artifact_collection = db.artifacts
artifact_collection.create_index("name", unique=True)


@ArtifactRegisterRouter.post("/code")
async def register_code_artifact(session: Session, user: IdentifiedUser, artifact: CodeArtifact):
    """Register code artifact"""

    return register_artifact(session, user, artifact)


@ArtifactRegisterRouter.post("/hyperparameters")
async def register_hyperparameters_artifact(session: Session, user: IdentifiedUser, artifact: HyperparametersArtifact):
    """Register hyperparameters artifact"""

    return register_artifact(session, user, artifact)


@ArtifactRegisterRouter.post("/dataset")
async def register_dataset_artifact(session: Session, user: IdentifiedUser, artifact: DatasetArtifact):
    """Register dataset artifact"""

    return register_artifact(session, user, artifact)


@ArtifactRegisterRouter.post("/model")
async def register_model_artifact(session: Session, user: IdentifiedUser, artifact: ModelArtifact):
    """Register model artifact"""

    return register_artifact(session, user, artifact)


@ArtifactRegisterRouter.post("/parameters")
async def register_parameters_artifact(session: Session, user: IdentifiedUser, artifact: ParametersArtifact):
    """Register parameters artifact"""

    return register_artifact(session, user, artifact)


@ArtifactRegisterRouter.post("/results")
async def register_results_artifact(session: Session, user: IdentifiedUser, artifact: ResultsArtifact):
    """Register results artifact"""

    return register_artifact(session, user, artifact)


def register_artifact(
    session: Session,
    user: IdentifiedUser,
    artifact: (
        CodeArtifact | HyperparametersArtifact | DatasetArtifact | ModelArtifact | ParametersArtifact | ResultsArtifact
    ),
):
    """Register artifacts of different types"""

    entry_data = artifact.model_dump()

    pipeline = entry_data.get("pipeline_name", None)
    source = entry_data.get("source_name", None)

    if source and not pipeline:
        return {"error": "Source artifact specified without pipeline."}
    if source:
        source_entry = artifact_collection.find_one({"name": entry_data["source_name"]})
        if not source_entry:
            return {"error": "Source artifact does not exist. Create the source artifact first."}

    artifact_exists = False
    can_modify = False
    update_flag = False
    with session.begin() as s:
        db_artifact = Artifact.get_artifact_by_name(session=s, artifact_name=artifact.name)

        if db_artifact:
            artifact_exists = True
            can_modify = db_artifact.can_modify(user.id)

    if (not artifact_exists) or can_modify:
        if entry_data.get("source_url"):
            entry_data["source_url"] = str(entry_data["source_url"])
        if entry_data.get("download_url"):
            entry_data["download_url"] = str(entry_data["download_url"])

        # remove pipeline-related logic
        entry_data.pop("pipeline_name", None)
        entry_data.pop("source_name", None)

        # If artifact does not exist in artifactdb, insert it
        if not artifact_exists:
            artifact_collection.insert_one(entry_data)
            print("New artifact inserted successfully in artifactdb.")

        # If user has the right to modify, update artifact
        else:
            artifact_collection.update_one({"name": artifact.name}, {"$set": entry_data})
            # note that at least the 'created_at' field will be updated
            print("Updated artifact successfully in artifactdb.")
            update_flag = True
    else:
        print("An artifact with this had been created by another user. A PermissionError will be returned.")

    # Handle dagdb operations (logic is inside the create method)
    node_data = ArtifactCreation(
        name=artifact.name,
        artifact_type=artifact.artifact_type,
        pipeline=pipeline,
        source=source,
    )

    try:
        with session.begin() as s:
            response = Artifact.create(session=s, param=node_data, user_id=user.id)
    except PermissionError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(err))

    if update_flag:
        response += "Artifact metadata updated successfully."

    return {"message": response}
