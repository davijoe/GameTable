from typing import List, Optional
from pydantic import BaseModel


class PersonRef(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class GameOut(BaseModel):
    id: int
    name: str
    image: Optional[str] = None
    thumbnail: Optional[str] = None
    min_players: Optional[int] = None
    max_players: Optional[int] = None
    minimum_age: Optional[int] = None
    playing_time: Optional[int] = None
    year_published: Optional[int] = None

    artists: List[PersonRef] = []
    designers: List[PersonRef] = []
    mechanics: List[PersonRef] = []
    genres: List[PersonRef] = []

    class Config:
        orm_mode = True
