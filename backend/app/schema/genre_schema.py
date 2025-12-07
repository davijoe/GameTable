from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, constr, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GenreBase(ORMModel):
    name: constr(min_length=1, max_length=30)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name is not only whitespace or only hyphens."""
        if not v.strip():
            raise ValueError("Name cannot be empty or only whitespace")
        if re.match(r"^-+$", v.strip()):
            raise ValueError("Name cannot be only hyphens")
        return v


class GenreCreate(GenreBase):
    pass


class GenreUpdate(ORMModel):
    name: constr(min_length=1, max_length=30) | None = None


class GenreRead(GenreBase):
    id: int
