from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, constr


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(ORMModel):
    display_name: constr(max_length=25)
    username: constr(max_length=255)
    email: EmailStr
    dob: date


class UserCreate(UserBase):
    password: constr(max_length=255)


class UserUpdate(ORMModel):
    display_name: Optional[constr(max_length=25)] = None
    username: Optional[constr(max_length=255)] = None
    email: Optional[EmailStr] = None
    dob: Optional[date] = None
    password: Optional[constr(max_length=255)] = None


class UserRead(UserBase):
    id: int

