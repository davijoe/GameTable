from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.genre_model import Genre


class GenreRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, genre_id: int) -> Optional[Genre]:
        return self.db.get(Genre, genre_id)

    def list(
        self, offset: int = 0, limit: int = 50, search: Optional[str] = None
    ) -> Tuple[List[Genre], int]:
        stmt = select(Genre)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(Genre.title.ilike(like))
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, genre: Genre) -> Genre:
        self.db.add(genre)
        self.db.flush()
        return genre

    def update(self, genre: Genre) -> Genre:
        self.db.merge(genre)
        self.db.flush()
        return genre

    def delete(self, genre: Genre) -> None:
        self.db.delete(genre)
        self.db.flush()

