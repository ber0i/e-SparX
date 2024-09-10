from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Table, select
from sqlalchemy.orm import (
    Mapped,
    Session,
    declarative_base,
    joinedload,
    mapped_column,
    relationship,
)

Base = declarative_base()


artifact_pipelines = Table(
    "artifact_pipelines",
    Base.metadata,
    Column("left_id", ForeignKey("artifacts.id"), primary_key=True),
    Column("right_id", ForeignKey("pipelines.id"), primary_key=True),
)

connection_sourceartifact = Table(
    "connection_sourceartifact",
    Base.metadata,
    Column("left_id", ForeignKey("connections.id"), primary_key=True),
    Column("right_id", ForeignKey("artifacts.id"), primary_key=True),
)

connection_targetartifact = Table(
    "connection_targetartifact",
    Base.metadata,
    Column("left_id", ForeignKey("connections.id"), primary_key=True),
    Column("right_id", ForeignKey("artifacts.id"), primary_key=True),
)

connection_pipeline = Table(
    "connection_pipeline",
    Base.metadata,
    Column("left_id", ForeignKey("connections.id"), primary_key=True),
    Column("right_id", ForeignKey("pipelines.id"), primary_key=True),
)


class ArtifactCreation(BaseModel):
    """Data needed for creating an artifact"""

    name: str
    """Name of the artifact"""

    pipeline: Optional[str] = None
    """List of pipeline names this artifact is part of"""


class ArtifactResponse(BaseModel):
    id: int
    name: str

    class Config:
        model_config = {"from_attributes": True}  # Use model_validate


class Artifact(Base):
    """Represenation of an artifact in the SQL/DAG database"""

    __tablename__ = "artifacts"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    """unique identifier of the artifact"""

    name: Mapped[str] = mapped_column("name", String, unique=True, nullable=False)
    """Unique artifact name"""

    pipelines: Mapped[List[Pipeline]] = relationship(secondary=artifact_pipelines, back_populates="artifacts")
    """List of pipelines the artifact is part of"""

    connections_as_source: Mapped[List[Connections]] = relationship(
        secondary=connection_sourceartifact, back_populates="source"
    )

    connections_as_target: Mapped[List[Connections]] = relationship(
        secondary=connection_targetartifact, back_populates="target"
    )

    @classmethod
    def read_by_name(cls, session: Session, name: str) -> "Artifact":
        """Read an artifact by name"""

        # define SQL statement
        stmt = select(cls).where(cls.name == name)
        return session.execute(stmt).scalar_one()

    @classmethod
    def read_by_id(cls, session: Session, id: int) -> "Artifact":
        """Read an artifact by id"""

        stmt = select(cls).where(cls.id == id)
        return session.execute(stmt).scalar_one()

    @classmethod
    def get_artifacts_by_pipeline(cls, session: Session, pipeline_name: str) -> List["Artifact"]:
        """Get all artifacts in a pipeline"""

        print(pipeline_name)
        stmt = (
            select(cls)
            .options(joinedload(cls.pipelines))
            .join(artifact_pipelines, cls.id == artifact_pipelines.c.left_id)  # Join artifacts with artifact_pipelines
            .join(Pipeline, artifact_pipelines.c.right_id == Pipeline.id)  # Join artifact_pipelines with pipelines
            .where(Pipeline.name == pipeline_name)  # Filter by pipeline name
        )
        print(stmt.compile(compile_kwargs={"literal_binds": True}))
        return session.execute(stmt).unique().scalars().all()

    @classmethod
    def create(cls, session: Session, param: ArtifactCreation) -> "Artifact":
        """Create a new artifact"""

        # If a pipeline was passed, retrieve it or create a new one
        if param.pipeline:
            pipeline_obj = session.query(Pipeline).filter_by(name=param.pipeline).first()
            if not pipeline_obj:
                print(f"Pipeline {param.pipeline} does not exist. Creating a new one.")
                pipeline_obj = Pipeline(name=param.pipeline)
                session.add(pipeline_obj)
                session.flush()
                print("New pipeline entry created.")

        # Check whether artifact exists in artifacts table
        artifact = session.query(Artifact).filter_by(name=param.name).first()

        if not artifact and not param.pipeline:
            artifact = Artifact(name=param.name)
            session.add(artifact)
            session.flush()
            response = f"Artifact {artifact.name} created without link to a pipeline."
        elif not artifact:
            artifact = Artifact(name=param.name, pipelines=[pipeline_obj])
            session.add(artifact)
            session.flush()
            response = f"Artifact {artifact.name} created and linked to pipeline {pipeline_obj.name}."
        else:
            artifact.pipelines.append(pipeline_obj)
            response = f"Artifact {artifact.name} found and linked to pipeline {pipeline_obj.name}."

        return response


class Pipeline(Base):
    """Represenation of a pipeline in the SQL/DAG database"""

    __tablename__ = "pipelines"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    """unique identifier of the pipeline"""

    name: Mapped[str] = mapped_column("name", String, unique=True, nullable=False)
    """Unique pipeline name"""

    artifacts: Mapped[List[Artifact]] = relationship(secondary=artifact_pipelines, back_populates="pipelines")

    connections: Mapped[List[Connections]] = relationship(secondary=connection_pipeline, back_populates="pipeline")


class Connections(Base):
    """Represenation of a connection between two artifacts in the SQL/DAG database"""

    __tablename__ = "connections"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    """unique identifier of the connection"""

    source: Mapped[Artifact] = relationship(secondary=connection_sourceartifact, back_populates="connections_as_source")
    """source artifact"""

    target: Mapped[Artifact] = relationship(secondary=connection_targetartifact, back_populates="connections_as_target")
    """target artifact"""

    pipeline: Mapped[Pipeline] = relationship(secondary=connection_pipeline, back_populates="connections")
    """corresponding pipeline"""
