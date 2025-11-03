from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, constr


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GenreBase(ORMModel):
    title: constr(max_length=30)
    description: Optional[constr(max_length=255)] = None


class GenreCreate(GenreBase):
    pass


class GenreUpdate(ORMModel):
    title: Optional[constr(max_length=30)] = None
    description: Optional[constr(max_length=255)] = None


class GenreRead(GenreBase):
    id: int

