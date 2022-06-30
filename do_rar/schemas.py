from pydantic import BaseModel


class OutputArchive(BaseModel):
    name: str
