from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)

    games = relationship(
        "Game",
        secondary="game_genres",
        back_populates="genres",
    )

    def __repr__(self) -> str:
        return f"<Genre id={self.id} name={self.name!r}>"
