from __future__ import annotations

from pydantic import BaseModel, ConfigDict, constr

from app.schema.user_schema import UserDisplayName


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReviewBase(ORMModel):
    title: constr(max_length=255)
    text: constr(max_length=255) | None = None
    star_amount: int
    user_id: int


class ReviewCreate(ReviewBase):
    game_id: int


class ReviewUpdate(ORMModel):
    title: constr(max_length=255) | None = None
    text: constr(max_length=255) | None = None
    star_amount: int | None = None
    user_id: int | None = None
    game_id: int | None = None


class ReviewRead(ORMModel):
    id: int
    title: constr(max_length=255)
    text: constr(max_length=255) | None = None
    star_amount: int
    user: UserDisplayName
    game_id: int
