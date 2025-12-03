from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Artist(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)

    # Many-to-many back to Game via game_artists table
    games = relationship(
        "Game",
        secondary="game_artists",
        back_populates="artists",
    )

    def __repr__(self) -> str:
        return f"<Artist id={self.id} name={self.name!r}>"
