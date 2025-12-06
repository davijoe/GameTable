from __future__ import annotations

from pydantic import BaseModel, ConfigDict, confloat, constr


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GameBase(ORMModel):
    name: constr(max_length=255)
    slug: constr(max_length=255) | None = None
    year_published: int | None = None
    bgg_rating: confloat() | None = None
    difficulty_rating: confloat() | None = None
    description: str | None = None
    playing_time: int | None = None
    available: bool | None = None
    min_players: int | None = None
    max_players: int | None = None
    image: str | None = None
    thumbnail: str | None = None


class GameCreate(GameBase):
    pass


class GameUpdate(ORMModel):
    name: constr(max_length=255) | None = None
    slug: constr(max_length=255) | None = None
    year_published: int | None = None
    difficulty_rating: confloat() | None = None
    description: str | None = None
    playing_time: int | None = None
    available: bool | None = None
    min_players: int | None = None
    max_players: int | None = None
    image: str | None = None
    thumbnail: str | None = None


class GameRead(GameBase):
    id: int
