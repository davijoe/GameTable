from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, constr, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(ORMModel):
    display_name: constr(max_length=25)
    username: constr(max_length=255)
    email: EmailStr
    dob: date

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
