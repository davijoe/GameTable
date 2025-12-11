from __future__ import annotations

from pydantic import BaseModel, ConfigDict, constr


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class VideoBase(ORMModel):
    title: constr(max_length=255)
    category: constr(max_length=255)
    link: constr(max_length=255)
    game_id: int
    language_id: int


class VideoCreate(VideoBase):
    pass


class VideoUpdate(VideoBase):
    title: constr(max_length=255) | None = None
    category: constr(max_length=255) | None = None
    link: constr(max_length=255) | None = None
    game_id: int | None = None
    language_id: int | None = None


class VideoRead(ORMModel):
    id: int
    title: str
    category: str
    link: str
    game_id: int
    language_id: int
