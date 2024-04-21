# Standard library imports
import os
import pathlib
from typing import TypeVar

import decouple

default_env_file = pathlib.Path(__file__).parents[3] / ".env"
env_file = os.environ.get("ENV_FILE", default_env_file)
env_config = decouple.Config(decouple.RepositoryEnv(env_file))


def as_bool(key: str, default: bool | None = None) -> bool:
    return bool(_get_value(key=key, default=default))


def as_int(key: str, default: int | None = None) -> int:
    return int(_get_value(key=key, default=default))


def as_str(key: str, default: str | None = None) -> str:
    return str(_get_value(key=key, default=default))


T = TypeVar("T")


def _get_value(key: str, default: T | None = None) -> T:
    return env_config.get(key, default)
