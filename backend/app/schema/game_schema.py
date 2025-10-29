from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict, constr, confloat

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class GameBase(ORMModel):
    name: constr(max_length=255)
    slug: Optional[constr(max_length=255)] = None
    year_published: Optional[constr(max_length=5)] = None
    bgg_rating: Optional[confloat()] = None
    difficulty_rating: Optional[confloat()] = None
    description: Optional[str] = None
    play_time: Optional[int] = None
    available: Optional[bool] = None
    min_players: Optional[int] = None
    max_players: Optional[int] = None

class GameCreate(GameBase):
    pass

class GameUpdate(ORMModel):
    name: Optional[constr(max_length=255)] = None
    slug: Optional[constr(max_length=255)] = None
    year_published: Optional[constr(max_length=5)] = None
    bgg_rating: Optional[confloat()] = None
    difficulty_rating: Optional[confloat()] = None
    description: Optional[str] = None
    play_time: Optional[int] = None
    available: Optional[bool] = None
    min_players: Optional[int] = None
    max_players: Optional[int] = None

class GameRead(GameBase):
    id: int
