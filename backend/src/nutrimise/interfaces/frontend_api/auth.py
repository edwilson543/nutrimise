import typing

import pydantic
from fastapi import param_functions


class User(pydantic.BaseModel):
    id: int


def get_authenticated_user() -> User:
    # TODO -> implement!
    return User(id=1)


AuthenticatedUser = typing.Annotated[
    User, param_functions.Depends(get_authenticated_user)
]
