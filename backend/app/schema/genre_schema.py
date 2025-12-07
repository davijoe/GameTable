from __future__ import annotations

from pydantic import BaseModel, ConfigDict, constr


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GenreBase(ORMModel):
    title: constr(max_length=30)
    description: constr(max_length=255) | None = None


class GenreCreate(GenreBase):
    pass


class GenreUpdate(ORMModel):
    title: constr(max_length=30) | None = None
    description: constr(max_length=255) | None = None


class GenreRead(GenreBase):
    id: int
