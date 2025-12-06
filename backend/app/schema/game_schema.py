from __future__ import annotations

from pydantic import BaseModel, ConfigDict, confloat, constr, field_validator


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GameBase(ORMModel):
    name: constr(min_length=1, max_length=255)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name is not empty, only whitespace, or only hyphens."""
        if not v or v.strip() == "":
            raise ValueError("Name cannot be empty or only whitespace")
        if all(c == "-" for c in v.strip()):
            raise ValueError("Name cannot be only hyphens")
        return v

    slug: constr(max_length=255) | None = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str | None) -> str | None:
        """Validate and normalize slug: no empty strings, convert to lowercase, replace spaces with hyphens."""
        if v is None:
            return v
        if v == "":
            raise ValueError("Slug cannot be empty string")
        if v.strip() == "":
            raise ValueError("Slug cannot be only whitespace")
        # Convert to lowercase and replace spaces with hyphens
        v = v.lower().replace(" ", "-")
        # After normalization, check if it's only hyphens
        if all(c == "-" for c in v):
            raise ValueError("Slug cannot be only hyphens")
        return v

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
