from __future__ import annotations

from pydantic import BaseModel, ConfigDict, constr, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LanguageBase(ORMModel):
    language: constr(max_length=255)

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Language cannot be empty or only whitespace")
        return v


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(LanguageBase):
    language: constr(max_length=255) | None = None

    @field_validator("language")
    @classmethod
    def validate_language_update(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("Language cannot be empty or only whitespace")
        return v


class LanguageRead(ORMModel):
    id: int
    language: str
