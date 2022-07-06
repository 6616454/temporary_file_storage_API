from uuid import UUID

from pydantic import BaseModel


class OutputArchive(BaseModel):
    name: str


class OutputFile(BaseModel):
    id: UUID
    name: str
    file: str
    link: str
    public: bool

    class Config:
        orm_mode = True


class UpdateFile(BaseModel):
    name: str | None
    public: bool | None
