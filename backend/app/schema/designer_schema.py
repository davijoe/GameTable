from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict, constr
from datetime import date


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DesignerBase(ORMModel):
    name: constr(max_length=255)
    dob: Optional[date] = None


class DesignerCreate(DesignerBase):
    pass


class DesignerUpdate(ORMModel):
    name: Optional[constr(max_length=255)] = None
    dob: Optional[date] = None


class DesignerRead(DesignerBase):
    id: int