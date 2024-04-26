from pydantic import BaseModel

class Response(BaseModel):

    openapi: str
    info: dict
    security: list
    paths: dict
    components: dict
