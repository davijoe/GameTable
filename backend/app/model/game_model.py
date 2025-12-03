from sqlalchemy import Boolean, Column, Double, Integer, String, Text

from app.utility.db import Base


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=True)
    year_published = Column(String(5), nullable=True)
    bgg_rating = Column(Double, nullable=True)
    difficulty_rating = Column(Double, nullable=True)
    description = Column(Text, nullable=True)
    play_time = Column(Integer, nullable=True)
    available = Column(Boolean, nullable=True)
    min_players = Column(Integer, nullable=True)
    max_players = Column(Integer, nullable=True)
    image = Column(String(1024), nullable=True)
    thumbnail = Column(String(1024), nullable=True)
