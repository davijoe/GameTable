from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.genre_model import Genre
from app.repository.genre.i_genre_repository import IGenreRepository


class SQLGenreRepository(IGenreRepository):
    def __init__(self, db: Session):
        self.db = db

    def get(self, genre_id: int) -> Genre | None:
        return self.db.get(Genre, genre_id)

    def get_by_name(self, name: str) -> Genre | None:
        return self.db.execute(
            select(Genre).where(Genre.name == name)
        ).scalar_one_or_none()

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[Genre], int]:
        stmt = select(Genre)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(Genre.name.ilike(like))
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, genre: Genre) -> Genre:
        self.db.add(genre)
        self.db.commit()
        return genre

    def update(self, genre: Genre) -> Genre:
        self.db.merge(genre)
        self.db.commit()
        return genre

    def delete(self, genre_id: int) -> None:
        genre = self.db.get(Genre, genre_id)
        if not genre:
            return False
        self.db.delete(genre)
        self.db.commit()
        return True
