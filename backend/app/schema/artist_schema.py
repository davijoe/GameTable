from __future__ import annotations

import re
from datetime import date

from pydantic import BaseModel, ConfigDict, constr, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ArtistBase(ORMModel):
    name: constr(min_length=1, max_length=255)
    dob: date | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty or only whitespace")
        if re.match(r"^-+$", v.strip()):
            raise ValueError("Name cannot be only hyphens")
        return v


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(ORMModel):
    name: constr(max_length=255) | None = None
    dob: date | None = None


class ArtistRead(ArtistBase):
    id: int
