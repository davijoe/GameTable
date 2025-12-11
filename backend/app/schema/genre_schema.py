from __future__ import annotations

from pydantic import BaseModel, ConfigDict, constr, field_validator

import re


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GenreBase(ORMModel):
    name: constr(min_length=1, max_length=30)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty or only whitespace")
        if re.match(r"^-+$", v.strip()):
            raise ValueError("Name cannot be only hyphens")
        return v


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    name: constr(min_length=1, max_length=30) | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Name cannot be empty or only whitespace")
        if re.match(r"^-+$", v.strip()):
            raise ValueError("Name cannot be only hyphens")
        return v


class GenreRead(ORMModel):
    id: int
    name: str
