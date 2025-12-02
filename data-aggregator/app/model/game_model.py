from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


game_artists = Table(
    "game_artists",
    Base.metadata,
    Column("game_id", ForeignKey("games.id"), primary_key=True),
    Column("artist_id", ForeignKey("artists.id"), primary_key=True),
)

game_designers = Table(
    "game_designers",
    Base.metadata,
    Column("game_id", ForeignKey("games.id"), primary_key=True),
    Column("designer_id", ForeignKey("designers.id"), primary_key=True),
)

game_mechanics = Table(
    "game_mechanics",
    Base.metadata,
    Column("game_id", ForeignKey("games.id"), primary_key=True),
    Column("mechanic_id", ForeignKey("mechanics.id"), primary_key=True),
)

game_genres = Table(
    "game_genres",
    Base.metadata,
    Column("game_id", ForeignKey("games.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False, index=True)

    image = Column(String(1024), nullable=True)
    thumbnail = Column(String(1024), nullable=True)

    min_players = Column(Integer, nullable=True)
    max_players = Column(Integer, nullable=True)
    minimum_age = Column(Integer, nullable=True)
    playing_time = Column(Integer, nullable=True)
    year_published = Column(Integer, nullable=True)

    # Relationships
    artists = relationship(
        "Artist",
        secondary="game_artists",
        back_populates="games",
        lazy="joined",
    )

    designers = relationship(
        "Designer",
        secondary="game_designers",
        back_populates="games",
        lazy="joined",
    )

    mechanics = relationship(
        "Mechanic",
        secondary="game_mechanics",
        back_populates="games",
        lazy="joined",
    )

    genres = relationship(
        "Genre",
        secondary="game_genres",
        back_populates="games",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"<Game id={self.id} name={self.name!r}>"
