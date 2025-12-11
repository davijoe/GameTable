from __future__ import annotations

from pydantic import BaseModel, ConfigDict, constr


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class LanguageBase(ORMModel):
    language: constr(max_length=255)


class LanguageCreate(LanguageBase):
    pass


class LanguageUpdate(LanguageBase):
    language: constr(max_length=255) | None = None


class LanguageRead(ORMModel):
    id: int
    language: str
