from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)

    # Many-to-many back to Game via game_publishers table
    games = relationship(
        "Game",
        secondary="game_publishers",
        back_populates="publishers",
    )

    def __repr__(self) -> str:
        return f"<Publisher id={self.id} name={self.name!r}>"
