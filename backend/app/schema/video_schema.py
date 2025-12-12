from __future__ import annotations

from pydantic import BaseModel, ConfigDict, constr, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class VideoBase(ORMModel):
    title: constr(max_length=255)

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty or only whitespace")
        return v

    category: constr(max_length=255)

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Category cannot be empty or only whitespace")
        return v

    link: constr(max_length=255)

    @field_validator("link")
    @classmethod
    def validate_link(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Link cannot be empty or only whitespace")
        return v

    game_id: int
    language_id: int


class VideoCreate(VideoBase):
    pass


class VideoUpdate(VideoBase):
    title: constr(max_length=255) | None = None

    @field_validator("title")
    @classmethod
    def validate_title_update(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or only whitespace")
        return v

    category: constr(max_length=255) | None = None

    @field_validator("category")
    @classmethod
    def validate_category_update(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Category cannot be empty or only whitespace")
        return v

    link: constr(max_length=255) | None = None

    @field_validator("link")
    @classmethod
    def validate_link_update(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Link cannot be empty or only whitespace")
        return v

    game_id: int | None = None
    language_id: int | None = None


class VideoRead(ORMModel):
    id: int
    title: str
    category: str
    link: str
    game_id: int
    language_id: int
