from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.model.artists_model import Artists


class ArtistRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, artist_id: int) -> Optional[Artists]:
        return self.db.get(Artists, artist_id)

    def list(
        self, offset: int = 0, limit: int = 50, search: Optional[str] = None
    ) -> Tuple[List[Artists], int]:
        stmt = select(Artists)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(Artists.name.ilike(like))
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, artist: Artists) -> Artists:
        self.db.add(artist)
        self.db.flush()
        return artist

    def update(self, artist: Artists) -> Artists:
        self.db.merge(artist)
        self.db.flush()
        return artist

    def delete(self, artist: Artists) -> None:
        self.db.delete(artist)
        self.db.flush()