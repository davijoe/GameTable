from __future__ import annotations

from datetime import date
import re

from pydantic import BaseModel, ConfigDict, EmailStr, constr, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(ORMModel):
    display_name: constr(max_length=55)

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Display name cannot be empty or only whitespace")
        return v

    username: constr(max_length=255)

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Username cannot be empty or only whitespace")
        return v

    email: EmailStr
    dob: date

    @field_validator("dob")
    @classmethod
    def validate_dob(cls, v: date | None) -> date | None:
        if v is None:
            return v
        min_date = date(1900, 1, 1)
        if v < min_date:
            raise ValueError("Date of birth must be on or after 01-01-1900")
        if v > date.today():
            raise ValueError("Date of birth cannot be in the future")
        return v


class UserCreate(UserBase):
    password: constr(min_length=6, max_length=255)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Password cannot be empty or only whitespace")
        return v


class UserUpdate(UserBase):
    display_name: constr(max_length=55) | None = None

    @field_validator("display_name")
    @classmethod
    def validate_display_name_update(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Display name cannot be empty or only whitespace")
        return v

    username: constr(max_length=255) | None = None

    @field_validator("username")
    @classmethod
    def validate_username_update(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Username cannot be empty or only whitespace")
        return v

    email: EmailStr | None = None
    dob: date | None = None

    @field_validator("dob")
    @classmethod
    def validate_dob_update(cls, v: date | None) -> date | None:
        if v is None:
            return v
        min_date = date(1900, 1, 1)
        if v < min_date:
            raise ValueError("DOB must be on or after 1900-01-01")
        if v > date.today():
            raise ValueError("DOB cannot be in the future")
        return v

    password: constr(min_length=6, max_length=255) | None = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Password cannot be empty or only whitespace")
        return v


class UserRead(ORMModel):
    id: int
    display_name: str
    username: str
    email: str
    dob: date
    is_admin: bool
