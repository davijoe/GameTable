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
        if not v.strip():
            raise ValueError("Name cannot be empty or only whitespace")
        if re.match(r"^-+$", v.strip()):
            raise ValueError("Name cannot be only hyphens")
        return v

    dob: date | None = None

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, v: date | None) -> date | None:
        if v is None:
            return v
        min_date = date(1900, 1, 1)
        if v < min_date:
            raise ValueError("DOB must be on or after 1900-01-01")
        if v > date.today():
            raise ValueError("DOB cannot be in the future")
        return v


class DesignerCreate(DesignerBase):
    pass


class DesignerUpdate(ORMModel):
    name: constr(max_length=255) | None = None
    dob: date | None = None


class DesignerRead(DesignerBase):
    id: int
