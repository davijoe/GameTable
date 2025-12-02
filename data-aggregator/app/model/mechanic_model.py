from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Mechanic(Base):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)

    games = relationship(
        "Game",
        secondary="game_mechanics",
        back_populates="mechanics",
    )

    def __repr__(self) -> str:
        return f"<Mechanic id={self.id} name={self.name!r}>"
