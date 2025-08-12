import pydantic


class Version(pydantic.BaseModel):
    version: str
