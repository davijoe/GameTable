from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, constr, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MechanicBase(ORMModel):
    name: constr(min_length=1, max_length=255)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be empty or only whitespace")
        if re.match(r"^-+$", v.strip()):
            raise ValueError("Name cannot be only hyphens")
        return v


class MechanicCreate(MechanicBase):
    pass


class MechanicUpdate(MechanicBase):
    name: constr(max_length=255) | None = None

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


class MechanicRead(ORMModel):
    id: int
    name: str
