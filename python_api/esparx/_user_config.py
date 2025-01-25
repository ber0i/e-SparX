import json
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

import platformdirs

user_config: "UserConfigModel" = None


@dataclass
class UserConfigModel:
    user_id: str
    api_base: str = "http://10.152.14.197:8443/api/"


def get_user_config_path():
    """Resolve the path to the user config file depending on the OS"""

    config_dir = platformdirs.user_config_dir("esparx", ensure_exists=True)
    return Path(config_dir) / "config.json"


def write_default_user_config(path: Path):
    """Write the default user config into the config file"""

    default_config = UserConfigModel(
        user_id=uuid4().hex
    )  # Generate config with random UUID

    write_user_config(path, default_config)
    return default_config


def write_user_config(path: Path, config: UserConfigModel):
    """Write new config to the config file"""
    global user_config

    config_dict = config.__dict__

    with open(path, mode="w+") as f:
        json.dump(config_dict, f, indent=2)

    user_config = config


def load_user_config(path: Path):
    """Load user config file from the given path"""
    global user_config

    with open(path, mode="r") as f:
        config_dict = json.load(f)

    user_config = UserConfigModel(**config_dict)
