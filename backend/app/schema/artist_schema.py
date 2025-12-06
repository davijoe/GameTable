from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, constr


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ArtistBase(ORMModel):
    name: constr(max_length=255)
    dob: date | None = None


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(ORMModel):
    name: constr(max_length=255) | None = None
    dob: date | None = None


class ArtistRead(ArtistBase):
    id: int
