from __future__ import annotations

from pydantic import BaseModel, ConfigDict, constr, field_validator

from app.schema.user_schema import UserDisplayName


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReviewBase(ORMModel):
    title: constr(max_length=255)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty or only whitespace")
        return v

    text: constr(max_length=255) | None = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Text cannot be empty or only whitespace")
        return v

    star_amount: int

    @field_validator("star_amount")
    @classmethod
    def validate_star_amount(cls, v: int) -> int:
        if v < 1 or v > 10:
            raise ValueError("Star amount must be between 1 and 10")
        return v

    user_id: int


class ReviewCreate(ReviewBase):
    game_id: int


class ReviewUpdate(ReviewBase):
    title: constr(max_length=255) | None = None

    @field_validator("title")
    @classmethod
    def validate_title_update(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or only whitespace")
        return v

    text: constr(max_length=255) | None = None

    @field_validator("text")
    @classmethod
    def validate_text_update(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Text cannot be empty or only whitespace")
        return v

    star_amount: int | None = None

    @field_validator("star_amount")
    @classmethod
    def validate_star_amount_update(cls, v: int | None) -> int | None:
        if v is not None and (v < 1 or v > 10):
            raise ValueError("Star amount must be between 1 and 10")
        return v

    user_id: int | None = None
    game_id: int | None = None


class ReviewRead(ORMModel):
    id: int
    title: str
    text: str | None = None
    star_amount: int
    user: UserDisplayName
    game_id: int
    user_id: int | None = None
