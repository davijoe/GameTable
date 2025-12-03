from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    category = Column(String(255), nullable=True)
    link = Column(String(255), nullable=False)

    # Many to one
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    game = relationship(
        "Game",
        back_populates="videos",
    )

    # Many to one - each video has a language
    language_id = Column(Integer, ForeignKey("language.id"), nullable=False)
    language = relationship("Language")
