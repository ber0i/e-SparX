import urllib.parse

from fastapi import APIRouter

from edl_api.dagdb import Session
from edl_api.documentdb import DocumentDBClient
from edl_api.schemas import Pipeline, Artifact

PipelineRouter = APIRouter(tags=["Pipelines"])

db = DocumentDBClient.artifactdb
artifact_collection = db.artifacts
artifact_collection.create_index("name", unique=True)


def pipeline_to_dict(pipeline: Pipeline) -> dict:
    return {
        "id": pipeline.id,
        "name": pipeline.name,
    }


@PipelineRouter.get("/")
async def get_pipelines(session: Session = Session):
    """Get all pipelines in the DAG database."""

    with session.begin() as s:
        pipelines = Pipeline.get_all_pipelines(s)
        pipeline_dicts = [pipeline_to_dict(pipeline) for pipeline in pipelines]
        return pipeline_dicts


@PipelineRouter.get("/artifact/{artifact_name}")
async def get_pipelines_by_artifact(artifact_name: str, session: Session = Session):
    """Get all pipelines in the DAG database that contain a specific artifact."""

    with session.begin() as s:
        pipelines = Pipeline.get_pipelines_by_artifact(s, artifact_name)
        pipeline_dicts = [pipeline_to_dict(pipeline) for pipeline in pipelines]
        return pipeline_dicts


@PipelineRouter.get("/results/{pipeline_name}")
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
