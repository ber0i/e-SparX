from fastapi import APIRouter

from edl_api.dagdb import Session
from edl_api.schemas import Pipeline

PipelineRouter = APIRouter(tags=["Pipelines"])


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
