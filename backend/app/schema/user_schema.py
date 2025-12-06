from __future__ import annotations

from datetime import date

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
    display_name: constr(max_length=25) | None = None
    username: constr(max_length=255) | None = None
    email: EmailStr | None = None
    dob: date | None = None
    password: constr(max_length=255) | None = None


class UserRead(UserBase):
    id: int
