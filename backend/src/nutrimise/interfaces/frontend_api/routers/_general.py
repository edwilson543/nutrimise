from importlib.metadata import version

from fastapi import responses, routing

from nutrimise.interfaces.frontend_api import schemas


general_router = routing.APIRouter()


@general_router.get("/health")
def get_health() -> responses.Response:
    return responses.Response()


@general_router.get("/version")
def get_version() -> schemas.Version:
    return schemas.Version(version=version("nutrimise"))
