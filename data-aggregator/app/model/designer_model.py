from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Designer(Base):
    __tablename__ = "designer"

    # many-to-many back to Game via game_designers
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)

    games = relationship(
        "Game",
        secondary="game_designers",
        back_populates="designers",
    )

    def __repr__(self) -> str:
        return f"<Designer id={self.id} name={self.name!r}>"
