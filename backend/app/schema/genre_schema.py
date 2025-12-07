from __future__ import annotations

from pydantic import BaseModel, ConfigDict, constr


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GenreBase(ORMModel):
    name: constr(min_length=1, max_length=30)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(ORMModel):
    name: constr(min_length=1, max_length=30) | None = None


class GenreRead(GenreBase):
    id: int
