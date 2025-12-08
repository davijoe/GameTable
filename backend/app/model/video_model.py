from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.utility.db_sql import Base


class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    link = Column(String(255), nullable=False)

    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
    language_id = Column(Integer, ForeignKey("language.id"), nullable=False)

    game = relationship("Game", back_populates="videos")
