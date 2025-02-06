import pydantic


class Recipe(pydantic.BaseModel):
    name: str
    description: str
