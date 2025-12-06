from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, constr


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DesignerBase(ORMModel):
    name: constr(max_length=255)
    dob: date | None = None


class DesignerCreate(DesignerBase):
    pass


class DesignerUpdate(ORMModel):
    name: constr(max_length=255) | None = None
    dob: date | None = None


class DesignerRead(DesignerBase):
    id: int
