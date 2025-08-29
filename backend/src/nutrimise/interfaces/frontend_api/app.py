import fastapi
from django.core import exceptions as django_exceptions
from fastapi.middleware import cors

from . import exception_handlers, routers


api = fastapi.FastAPI()

api.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api.include_router(routers.general_router, prefix="/general")
api.include_router(routers.recipe_router, prefix="/recipes")

api.add_exception_handler(
    django_exceptions.ObjectDoesNotExist, exception_handlers.object_does_not_exist
)
