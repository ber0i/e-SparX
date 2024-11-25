"""This file enables accessing environment variables."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # define variables which should be read from .env
    ARTIFACTDB_ENDPOINT: str
    DAGDB_CONNECTSTRING: str

    # define the path to the .env file
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        case_sensitive=True,
    )


# instantiate the settings object, which will read the .env file
settings = Settings()
