from __future__ import annotations

import re

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    confloat,
    constr,
    field_validator,
)

from app.schema.artist_schema import ArtistRead
from app.schema.designer_schema import DesignerRead
from app.schema.mechanic_schema import MechanicRead
from app.schema.publisher_schema import PublisherRead

MAX_BYTES = 65535


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class GameBase(ORMModel):
    name: constr(min_length=1, max_length=255)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that name is not only whitespace or only hyphens."""
        if not v.strip():
            raise ValueError("Name cannot be empty or only whitespace")
        if re.match(r"^-+$", v.strip()):
            raise ValueError("Name cannot be only hyphens")
        return v

    slug: constr(min_length=1, max_length=255) | None = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str | None) -> str | None:
        """Validate and normalize slug: no empty strings, convert to lowercase, replace spaces with hyphens."""
        if v is None:
            return v
        if not v.strip():
            raise ValueError("Slug cannot be empty or only whitespace")
        # Normalize: convert to lowercase and replace spaces with hyphens
        v = v.lower().replace(" ", "-")
        if re.match(r"^-+$", v):
            raise ValueError("Slug cannot be only hyphens")
        return v

    year_published: int | None = Field(None, ge=1901, le=2155)

    bgg_rating: confloat(ge=1, le=10) | None = None

    @field_validator("bgg_rating")
    @classmethod
    def validate_bgg_rating(cls, v: float | None) -> float | None:
        """Validate that bgg_rating has at most 2 decimal places."""
        if v is None:
            return v
        if len(str(v).split(".")[-1]) > 2:
            raise ValueError("BGG rating must have at most 2 decimal places")
        return v

    difficulty_rating: confloat(ge=1, le=5) | None = None

    @field_validator("difficulty_rating")
    @classmethod
    def validate_difficulty_rating(cls, v: float | None) -> float | None:
        """Validate that difficulty_rating has at most 2 decimal places."""
        if v is None:
            return v
        if len(str(v).split(".")[-1]) > 2:
            raise ValueError("Difficulty rating must have at most 2 decimal places")
        return v

    playing_time: int | None = None
    description: str | None = Field(None, min_length=1)

    @field_validator("description")
    @classmethod
    def validate_desc_byte_size(cls, v: str) -> str:
        byte_len = len(v.encode("utf-8"))
        if byte_len > MAX_BYTES:
            raise ValueError(
                f"Description is too long: byte length {byte_len} exceeds {MAX_BYTES}"
            )
        return v

    min_players: int | None = Field(None, ge=1, le=999)
    max_players: int | None = Field(None, ge=1, le=999)
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
    min_players: int | None = Field(None, ge=1, le=999)
    max_players: int | None = Field(None, ge=1, le=999)
    image: str | None = None
    thumbnail: str | None = None


class GameRead(GameBase):
    id: int


# GameDetail is used when end user clicks on a game - uses join table
class GameDetail(GameRead):
    artists: list[ArtistRead] = []
    designers: list[DesignerRead] = []
    publishers: list[PublisherRead] = []
    mechanics: list[MechanicRead] = []
