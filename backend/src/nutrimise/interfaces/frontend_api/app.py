import fastapi

from . import routers


api = fastapi.FastAPI()

api.include_router(routers.general_router, prefix="/general")
api.include_router(routers.recipe_router, prefix="/recipes")
