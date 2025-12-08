from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.artists_model import Artist


class SQLArtistRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, artist_id: int) -> Artist | None:
        return self.db.get(Artist, artist_id)

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[Artist], int]:
        stmt = select(Artist)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(Artist.name.ilike(like))
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, artist: Artist) -> Artist:
        self.db.add(artist)
        self.db.flush()
        return artist

    def update(self, artist: Artist) -> Artist:
        self.db.merge(artist)
        self.db.flush()
        return artist

    def delete(self, artist: Artist) -> None:
        self.db.delete(artist)
        self.db.flush()
