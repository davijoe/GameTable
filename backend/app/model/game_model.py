from sqlalchemy import Column, Double, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from app.model.artists_model import Artist
from app.model.designer_model import Designer
from app.model.mechanic_model import Mechanic
from app.model.publisher_model import Publisher
from app.model.video_model import Video
from app.utility.db_sql import Base

game_artists = Table(
    "game_artists",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("game.id"), primary_key=True),
    Column("artist_id", Integer, ForeignKey("artist.id"), primary_key=True),
)

game_designers = Table(
    "game_designers",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("game.id"), primary_key=True),
    Column("designer_id", Integer, ForeignKey("designer.id"), primary_key=True),
)
game_publishers = Table(
    "game_publishers",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("game.id"), primary_key=True),
    Column("publisher_id", Integer, ForeignKey("publisher.id"), primary_key=True),
)

game_mechanics = Table(
    "game_mechanics",
    Base.metadata,
    Column("game_id", Integer, ForeignKey("game.id"), primary_key=True),
    Column("mechanic_id", Integer, ForeignKey("mechanic.id"), primary_key=True),
)

class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=True)
    year_published = Column(String(5), nullable=True)
    bgg_rating = Column(Double, nullable=True)
    difficulty_rating = Column(Double, nullable=True)
    description = Column(Text, nullable=True)
    playing_time = Column(Integer, nullable=True)
    min_players = Column(Integer, nullable=True)
    max_players = Column(Integer, nullable=True)
    image = Column(String(1024), nullable=True)
    thumbnail = Column(String(1024), nullable=True)

    artists = relationship(Artist, secondary=game_artists, lazy="select")
    designers = relationship(Designer, secondary=game_designers, lazy="select")
    publishers = relationship(Publisher, secondary=game_publishers, lazy="select")
    mechanics = relationship(Mechanic, secondary=game_mechanics, lazy="select")
    videos = relationship(Video, back_populates="game", lazy="select")
