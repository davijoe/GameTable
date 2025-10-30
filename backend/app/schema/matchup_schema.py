from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class MatchupBase(ORMModel):
    game_id: int
    is_private: bool
    user_id_winner: int
    user_id_1: int
    user_id_2: int
    start_time: Optional[date] = None
    end_time: Optional[date] = None
    created_at: Optional[date] = None
    created_by_user_id: Optional[int] = None


class MatchupCreate(MatchupBase):
    pass


class MatchupUpdate(ORMModel):
    game_id: Optional[int] = None
    is_private: Optional[bool] = None
    user_id_winner: Optional[int] = None
    user_id_1: Optional[int] = None
    user_id_2: Optional[int] = None
    start_time: Optional[date] = None
    end_time: Optional[date] = None
    created_at: Optional[date] = None
    created_by_user_id: Optional[int] = None


class MatchupRead(MatchupBase):
    id: int