from importlib.metadata import version

import fastapi
from fastapi import responses

from nutrimise.interfaces.frontend_api import schemas


general_router = fastapi.APIRouter()


@general_router.get("/health")
def get_health() -> responses.Response:
    return responses.Response()


@general_router.get("/version")
def get_version() -> schemas.Version:
    return schemas.Version(version=version("nutrimise"))
