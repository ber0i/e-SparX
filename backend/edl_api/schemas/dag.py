from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Table, and_, select
from sqlalchemy.orm import (
    Mapped,
    Session,
    aliased,
    declarative_base,
    joinedload,
    mapped_column,
    relationship,
)

# Define ANSI color codes
COLORS = {
    "artifact": "\033[94m",  # Blue
    "pipeline": "\033[95m",  # Magenta
    "created": "\033[1;92m",  # Green
    "connected": "\033[1;93m",  # Yellow
    "deleted": "\033[1;91m",  # Red
    "reset": "\033[0m",  # Reset color
}

Base = declarative_base()


artifact_pipelines = Table(
    "artifact_pipelines",
    Base.metadata,
    Column("left_id", ForeignKey("artifacts.id", ondelete="CASCADE"), primary_key=True),
    Column("right_id", ForeignKey("pipelines.id", ondelete="CASCADE"), primary_key=True),
)

connection_sourceartifact = Table(
    "connection_sourceartifact",
    Base.metadata,
    Column("left_id", ForeignKey("connections.id", ondelete="CASCADE"), primary_key=True),
    Column("right_id", ForeignKey("artifacts.id", ondelete="CASCADE"), primary_key=True),
)

connection_targetartifact = Table(
    "connection_targetartifact",
    Base.metadata,
    Column("left_id", ForeignKey("connections.id", ondelete="CASCADE"), primary_key=True),
    Column("right_id", ForeignKey("artifacts.id", ondelete="CASCADE"), primary_key=True),
)

connection_pipeline = Table(
    "connection_pipeline",
    Base.metadata,
    Column("left_id", ForeignKey("connections.id", ondelete="CASCADE"), primary_key=True),
    Column("right_id", ForeignKey("pipelines.id", ondelete="CASCADE"), primary_key=True),
)


class ArtifactCreation(BaseModel):
    """Data needed for creating an artifact"""

    name: str
    """Name of the artifact"""

    artifact_type: str
    """Type of the artifact. Can be "dataset" or "code"."""

    pipeline: Optional[str] = None
    """Pipeline names this artifact should be linked to"""

    parent: Optional[str] = None
    """Name of the parent artifact in pipeline"""


class ConnectionCreation(BaseModel):
    """Schema for a connection"""

    source: str
    target: str
    pipeline: str


class ArtifactResponse(BaseModel):
    id: int
    name: str
    artifact_type: str

    class Config:
        model_config = {"from_attributes": True}  # Use model_validate


class ArtifactResponseForConnections(BaseModel):
    name: str


class ConnectionResponse(BaseModel):
    source: ArtifactResponseForConnections
    target: ArtifactResponseForConnections


class Artifact(Base):
    """Represenation of an artifact in the SQL/DAG database"""

    __tablename__ = "artifacts"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    """unique identifier of the artifact"""

    owner_id: Mapped[str] = mapped_column("owner_id", String, unique=False, nullable=False)
    """unique identifier of the owner of the artifact"""

    name: Mapped[str] = mapped_column("name", String, unique=True, nullable=False)
    """Unique artifact name"""

    artifact_type: Mapped[str] = mapped_column("artifact_type", String, nullable=False)
    """Type of the artifact."""

    pipelines: Mapped[List[Pipeline]] = relationship(
        secondary=artifact_pipelines, back_populates="artifacts", cascade="all, delete"
    )
    """
    List of pipelines the artifact is part of.
    When an artifact is deleted, the link to the pipeline is also deleted.
    """

    connections_as_source: Mapped[List[Connection]] = relationship(
        secondary=connection_sourceartifact, back_populates="source", cascade="all, delete"
    )

    connections_as_target: Mapped[List[Connection]] = relationship(
        secondary=connection_targetartifact, back_populates="target", cascade="all, delete"
    )

    def can_modify(self, user_id: str) -> bool:
        """Checks if a given user is allowed to modify the artifact"""

        return self.owner_id == user_id

    @classmethod
    def get_all_artifacts(cls, session: Session) -> List["Artifact"]:
        """Get all artifacts"""

        return session.query(cls).all()

    @classmethod
    def get_results_artifacts_by_pipeline(cls, session: Session, pipeline_name: str) -> List["Artifact"]:
        """Get all results artifacts in a pipeline"""

        stmt = (
            select(cls)
            .options(joinedload(cls.pipelines))
            .join(artifact_pipelines, cls.id == artifact_pipelines.c.left_id)  # Join artifacts with artifact_pipelines
            .join(Pipeline, artifact_pipelines.c.right_id == Pipeline.id)  # Join artifact_pipelines with pipelines
            .where(Pipeline.name == pipeline_name)  # Filter by pipeline name
            .where(cls.artifact_type == "results")  # Filter by artifact type
        )
        return session.execute(stmt).unique().scalars().all()

    @classmethod
    def create(cls, session: Session, param: ArtifactCreation, user_id: str) -> str:
        """
        Dagdb operation to create an artifact and link it to a pipeline.
        See Miro graphic for underlying logic.
        """

        artifact = session.query(Artifact).filter_by(name=param.name).first()
        if not artifact:
            artifact = Artifact(name=param.name, artifact_type=param.artifact_type, owner_id=user_id)
            session.add(artifact)
            session.flush()
            print(f"Artifact '{artifact.name}' created.")
            response = f"{COLORS['created']}CREATED{COLORS['reset']} artifact {COLORS['artifact']}{artifact.name}{COLORS['reset']}.\n"  # noqa: E501
        else:
            print(f"Artifact '{artifact.name}' already exists.")
            response = f"Artifact {COLORS['artifact']}{artifact.name}{COLORS['reset']} already exists.\n"

        if not param.pipeline:
            print("No pipeline linked.")
            response += "No pipeline linked.\n"  # Done.

        else:
            pipeline = session.query(Pipeline).filter_by(name=param.pipeline).first()
            if not pipeline:
                pipeline = Pipeline(name=param.pipeline, artifacts=[artifact], owner_id=user_id)
                session.add(pipeline)
                session.flush()
                print(f"Pipeline '{pipeline.name}' created and linked to artifact '{artifact.name}'.")
                response += f"{COLORS['created']}CREATED{COLORS['reset']} pipeline {COLORS['pipeline']}{pipeline.name}{COLORS['reset']}.\n"
                response += f"{COLORS['connected']}CONNECTED{COLORS['reset']} artifact {COLORS['artifact']}{artifact.name}{COLORS['reset']} to pipeline {COLORS['pipeline']}{pipeline.name}{COLORS['reset']}.\n"  # noqa: E501

            else:
                if not pipeline.can_modify(user_id):
                    raise PermissionError("Whoops! Users can only modify pipelines they've created themselves!")

                response += f"Pipeline {COLORS['pipeline']}{pipeline.name}{COLORS['reset']} found.\n"
                if pipeline not in artifact.pipelines:
                    artifact.pipelines.append(pipeline)
                    print(f"Pipeline '{pipeline.name}' found and linked to artifact '{artifact.name}'.")
                    response += f"{COLORS['connected']}CONNECTED{COLORS['reset']} artifact {COLORS['artifact']}{artifact.name}{COLORS['reset']} to pipeline {COLORS['pipeline']}{pipeline.name}{COLORS['reset']}.\n"  # noqa: E501
                else:
                    print(f"Pipeline '{pipeline.name}' found, and it is already linked to artifact '{artifact.name}'.")
                    response += f"Artifact {COLORS['artifact']}{artifact.name}{COLORS['reset']} is already linked to pipeline {COLORS['pipeline']}{pipeline.name}{COLORS['reset']}.\n"  # Done. # noqa: E501

            if param.parent:
                parent = session.query(Artifact).filter_by(name=param.parent).first()

                # Aliases for clearer joins
                SourceArtifact = aliased(Artifact, name="source_artifact")
                TargetArtifact = aliased(Artifact, name="target_artifact")

                # Query for existing connection
                connection = (
                    session.query(Connection)
                    .join(connection_sourceartifact, connection_sourceartifact.c.left_id == Connection.id)
                    .join(SourceArtifact, connection_sourceartifact.c.right_id == SourceArtifact.id)
                    .join(connection_targetartifact, connection_targetartifact.c.left_id == Connection.id)
                    .join(TargetArtifact, connection_targetartifact.c.right_id == TargetArtifact.id)
                    .filter(
                        and_(
                            SourceArtifact.id == parent.id,
                            TargetArtifact.id == artifact.id,
                            Connection.pipeline == pipeline,
                        )
                    )
                    .first()
                )
                if not connection:
                    parent = session.query(Artifact).filter_by(name=param.parent).first()
                    connection = Connection(source=parent, target=artifact, pipeline=pipeline)
                    session.add(connection)
                    session.flush()
                    print(
                        f"Connection between '{param.parent}' and '{param.name}' created within pipeline '{param.pipeline}'."
                    )
                    response += f"{COLORS['connected']}CONNECTED{COLORS['reset']} {COLORS['artifact']}{param.parent}{COLORS['reset']} to {COLORS['artifact']}{param.name}{COLORS['reset']} within pipeline {COLORS['pipeline']}{param.pipeline}{COLORS['reset']}.\n"  # noqa: E501
                    # Check whether the connection parent is linked to the pipeline
                    if parent not in pipeline.artifacts:
                        parent.pipelines.append(pipeline)
                        print(
                            f"For this, the parent artifact '{parent.name}' was linked to pipeline '{pipeline.name}', as this connection had not been established yet."  # noqa: E501
                        )
                        response += f"Artifact {COLORS['artifact']}{parent.name}{COLORS['reset']} has not yet been linked to pipeline {COLORS['pipeline']}{pipeline.name}{COLORS['reset']}.\n"  # noqa: E501
                        response += f"{COLORS['connected']}CONNECTED{COLORS['reset']} artifact {COLORS['artifact']}{parent.name}{COLORS['reset']} to pipeline {COLORS['pipeline']}{pipeline.name}{COLORS['reset']}.\n"  # noqa: E501
                else:
                    print(
                        f"Connection between '{param.parent}' and '{param.name}' already exists in pipeline '{param.pipeline}'."
                    )
                    response += f"Connection between {COLORS['artifact']}{param.parent}{COLORS['reset']} and {COLORS['artifact']}{param.name}{COLORS['reset']} already exists within pipeline {COLORS['pipeline']}{param.pipeline}{COLORS['reset']}.\n"  # Done. # noqa: E501

        return response


class Pipeline(Base):
    """Represenation of a pipeline in the SQL/DAG database"""

    __tablename__ = "pipelines"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    """unique identifier of the pipeline"""

    owner_id: Mapped[str] = mapped_column("owner_id", String, unique=False, nullable=False)
    """unique identifier of the owner of the artifact"""

    name: Mapped[str] = mapped_column("name", String, unique=True, nullable=False)
    """Unique pipeline name"""

    artifacts: Mapped[List[Artifact]] = relationship(
        secondary=artifact_pipelines, back_populates="pipelines", cascade="all, delete"
    )

    connections: Mapped[List[Connection]] = relationship(
        secondary=connection_pipeline, back_populates="pipeline", cascade="all, delete"
    )

    def can_modify(self, user_id: str) -> bool:
        """Checks if a given user is allowed to modify the pipeline"""

        return self.owner_id == user_id

    @classmethod
    def get_all_pipelines(cls, session: Session) -> List["Pipeline"]:
        """Get all pipelines"""

        return session.query(cls).all()

    @classmethod
    def get_pipelines_by_artifact(cls, session: Session, artifact_name: str) -> List["Pipeline"]:
        """Get all pipelines that contain a specific artifact"""

        stmt = (
            select(cls)
            .options(joinedload(cls.artifacts))
            .join(artifact_pipelines, cls.id == artifact_pipelines.c.right_id)  # Join pipelines with artifact_pipelines
            .join(Artifact, artifact_pipelines.c.left_id == Artifact.id)  # Join artifact_pipelines with artifacts
            .where(Artifact.name == artifact_name)  # Filter by artifact name
        )
        return session.execute(stmt).unique().scalars().all()


class Connection(Base):
    """Represenation of a connection between two artifacts in the SQL/DAG database"""

    __tablename__ = "connections"

    id: Mapped[int] = mapped_column("id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    """unique identifier of the connection"""

    source: Mapped[Artifact] = relationship(
        secondary=connection_sourceartifact, back_populates="connections_as_source", cascade="all, delete"
    )
    """source artifact"""

    target: Mapped[Artifact] = relationship(
        secondary=connection_targetartifact, back_populates="connections_as_target", cascade="all, delete"
    )
    """target artifact"""

    pipeline: Mapped[Pipeline] = relationship(
        secondary=connection_pipeline, back_populates="connections", cascade="all, delete"
    )
    """corresponding pipeline"""

    def can_modify(self, user_id: str) -> bool:
        """Checks if a given user is allowed to modify the connection"""

        return self.pipeline.can_modify(user_id)

    @classmethod
    def get_all_connections(cls, session: Session) -> List["Connection"]:
        """Get all connections"""

        return session.query(cls).all()

    @classmethod
    def create(cls, session: Session, param: ConnectionCreation, user_id: str) -> str:
        """
        Dagdb operation to create a connection between two existing artifacts.
        If one of the two artifacts is not linked to the pipeline, the link will be created.
        """

        source_artifact = session.query(Artifact).filter_by(name=param.source).first()
        if not source_artifact:
            print(f"Artifact '{param.source}' not found.")
            raise ValueError(f"Artifact '{param.source}' not found.")

        target_artifact = session.query(Artifact).filter_by(name=param.target).first()
        if not target_artifact:
            print(f"Artifact '{param.target}' not found.")
            raise ValueError(f"Artifact '{param.target}' not found.")

        pipeline = session.query(Pipeline).filter_by(name=param.pipeline).first()
        if not pipeline:
            print(f"Pipeline '{param.pipeline}' not found.")
            raise ValueError(f"Pipeline '{param.pipeline}' not found.")

        response = ""

        if pipeline not in source_artifact.pipelines:
            source_artifact.pipelines.append(pipeline)
            print(
                f"The source artifact '{source_artifact.name}' was not linked to pipeline '{pipeline.name}' yet. This link was now created."
            )
            response += f"The source artifact {COLORS['artifact']}{source_artifact.name}{COLORS['reset']} was not linked to pipeline {COLORS['pipeline']}{pipeline.name}{COLORS['reset']} yet.\n"  # noqa: E501
            response += f"{COLORS['connected']}CONNECTED{COLORS['reset']} artifact {COLORS['artifact']}{source_artifact.name}{COLORS['reset']} to pipeline {COLORS['pipeline']}{pipeline.name}{COLORS['reset']}.\n"  # noqa: E501

        if pipeline not in target_artifact.pipelines:
            target_artifact.pipelines.append(pipeline)
            print(
                f"The target artifact '{target_artifact.name}' was not linked to pipeline '{pipeline.name}' yet. This link was now created."
            )
            response += f"The target artifact {COLORS['artifact']}{target_artifact.name}{COLORS['reset']} was not linked to pipeline {COLORS['pipeline']}{pipeline.name}{COLORS['reset']} yet.\n"  # noqa: E501
            response += f"{COLORS['connected']}CONNECTED{COLORS['reset']} artifact {COLORS['artifact']}{target_artifact.name}{COLORS['reset']} to pipeline {COLORS['pipeline']}{pipeline.name}{COLORS['reset']}.\n"  # noqa: E501

        if not pipeline.can_modify(user_id):
            raise PermissionError("Whoops! Users can only modify pipelines they've created themselves!")

        # Aliases for clearer joins
        SourceArtifact = aliased(Artifact, name="source_artifact")
        TargetArtifact = aliased(Artifact, name="target_artifact")

        # Query for existing connection
        connection = (
            session.query(Connection)
            .join(connection_sourceartifact, connection_sourceartifact.c.left_id == Connection.id)
            .join(SourceArtifact, connection_sourceartifact.c.right_id == SourceArtifact.id)
            .join(connection_targetartifact, connection_targetartifact.c.left_id == Connection.id)
            .join(TargetArtifact, connection_targetartifact.c.right_id == TargetArtifact.id)
            .filter(
                and_(
                    SourceArtifact.id == source_artifact.id,
                    TargetArtifact.id == target_artifact.id,
                    Connection.pipeline == pipeline,
                )
            )
            .first()
        )
        if not connection:
            connection = Connection(source=source_artifact, target=target_artifact, pipeline=pipeline)
            session.add(connection)
            session.flush()
            print(
                f"Connection between '{param.source}' and '{param.target}' created within pipeline '{param.pipeline}'."
            )
            response += f"{COLORS['connected']}CONNECTED{COLORS['reset']} {COLORS['artifact']}{param.source}{COLORS['reset']} to {COLORS['artifact']}{param.target}{COLORS['reset']} within pipeline {COLORS['pipeline']}{param.pipeline}{COLORS['reset']}.\n"  # Done. # noqa: E501
        else:
            print(
                f"Connection between '{param.source}' and '{param.target}' already exists in pipeline '{param.pipeline}'."
            )
            response += f"Connection between {COLORS['artifact']}{param.source}{COLORS['reset']} and {COLORS['artifact']}{param.target}{COLORS['reset']} already exists within pipeline {COLORS['pipeline']}{param.pipeline}{COLORS['reset']}.\n"  # Done. # noqa: E501

        return response
