import fastapi

from . import routers


api = fastapi.FastAPI()

api.include_router(routers.general_router, prefix="/general")
