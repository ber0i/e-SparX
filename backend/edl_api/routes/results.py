import urllib.parse

from fastapi import APIRouter, HTTPException, status

from edl_api.dagdb import Session
from edl_api.dependencies.auth import IdentifiedUser
from edl_api.documentdb import DocumentDBClient
from edl_api.schemas import Artifact, ArtifactCreation, ResultsArtifact

ResultsArtifactRouter = APIRouter(tags=["Results Artifacts"])

db = DocumentDBClient.artifactdb
artifact_collection = db.artifacts
artifact_collection.create_index("name", unique=True)


def artifact_to_dict(artifact: Artifact) -> dict:
    return {
        "id": artifact.id,
        "name": artifact.name,
        "artifact_type": artifact.artifact_type,
    }


@ResultsArtifactRouter.post("/")
async def register_results_artifact(results: ResultsArtifact, session: Session, user: IdentifiedUser):
    """Register a hyperparameters artifact."""

    entry_data = results.model_dump()
    pipeline = entry_data["pipeline_name"] if entry_data["pipeline_name"] else None
    source = entry_data["source_name"] if entry_data["source_name"] else None

    if source and not pipeline:
        return {"error": "Source artifact specified without pipeline."}
    if source:
        source_entry = artifact_collection.find_one({"name": entry_data["source_name"]})
        if not source_entry:
            return {"error": "Source artifact does not exist. Create the source artifact first."}

    # If artifact does not exist in artifactdb, insert it
    existing_entry = artifact_collection.find_one({"name": entry_data["name"]})
    if not existing_entry:
        # remove pipeline-related logic
        entry_data.pop("pipeline_name", None)
        entry_data.pop("source_name", None)
        artifact_collection.insert_one(entry_data)
        print("New artifact inserted successfully in artifactdb.")
    else:
        print("Artifact already exists in artifactdb.")

    # Handle dagdb operations (logic is inside the create method)
    node_data = ArtifactCreation(
        name=entry_data["name"], artifact_type=entry_data["artifact_type"], pipeline=pipeline, source=source
    )

    try:
        with session.begin() as s:
            response = Artifact.create(session=s, param=node_data, user_id=user.id)
    except PermissionError as err:
        return HTTPException(status.HTTP_401_UNAUTHORIZED, err)

    return {"message": response}


@ResultsArtifactRouter.get("/pipeline/{pipeline_name}")
async def get_results_artifacts_by_pipeline(pipeline_name: str, session: Session = Session):
    """Get all results artifacts in a pipeline"""

    pipeline_name = urllib.parse.unquote(pipeline_name)
    results_artifacts_name_list = []
    results_metrics_list = []
    results_valuelists_list = []
    # Search for the artifacts in the database collection
    with session.begin() as s:
        results_artifacts = Artifact.get_results_artifacts_by_pipeline(s, pipeline_name)
        for result_artifact in results_artifacts:
            results_artifacts_name_list.append(result_artifact.name)
            # get artifact by name
            artifact = artifact_collection.find_one({"name": result_artifact.name}, {"_id": 0})
            results = artifact["results"]
            results_values_list = []
            for result in results:
                results_metrics_list.append(result["metric"])
                results_values_list.append(result["value"])
            results_valuelists_list.append(results_values_list)

    # always put 'persistence' as the first metric
    # TODO: This solution does not generalize well, implement a more sophisticated solution
    if "Persistence Results" in results_artifacts_name_list:
        keep_values = results_valuelists_list[results_artifacts_name_list.index("Persistence Results")]
        results_valuelists_list.remove(keep_values)
        results_valuelists_list.insert(0, keep_values)
        results_artifacts_name_list.remove("Persistence Results")
        results_artifacts_name_list.insert(0, "Persistence Results")

    # define a new list where each element is a list of values for a metric
    # the order of the values must fit to the name list, i.e.,
    # list[0] corrsponds to list(set(results_metrics_list))[0]
    # and element 0 in list[0] corresponds to results_artifacts_name_list[0]
    value_list_by_metric = []
    for metric in list(set(results_metrics_list)):
        value_list = []
        for i in range(len(results_artifacts_name_list)):
            value_list.append(results_valuelists_list[i][results_metrics_list.index(metric)])
        value_list_by_metric.append(value_list)

    response = {
        "results_artifacts_names": results_artifacts_name_list,
        "results_metrics": list(set(results_metrics_list)),
        "results_values": value_list_by_metric,
    }
    print(results_artifacts_name_list)

    return response
