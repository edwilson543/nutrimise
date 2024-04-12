# Standard library imports
import os
from typing import Type

from configurations.importer import install
from mypy_django_plugin import main


def plugin(version: str) -> Type[main.NewSemanalDjangoPlugin]:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reciply.config.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Settings")
    install()
    return main.plugin(version)
