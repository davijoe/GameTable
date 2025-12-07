from __future__ import annotations

from datetime import date
import re

from pydantic import BaseModel, ConfigDict, constr, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DesignerBase(ORMModel):
    name: constr(min_length=1, max_length=255)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name is not only whitespace or only hyphens."""
        if not v.strip():
            raise ValueError("Name cannot be empty or only whitespace")
        if re.match(r"^-+$", v.strip()):
            raise ValueError("Name cannot be only hyphens")
        return v

    dob: date | None = None


class DesignerCreate(DesignerBase):
    pass


class DesignerUpdate(ORMModel):
    name: constr(max_length=255) | None = None
    dob: date | None = None


class DesignerRead(DesignerBase):
    id: int
