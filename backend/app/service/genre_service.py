from sqlalchemy.orm import Session

from app.model.genre_model import Genre
from app.repository.genre.sql_genre_repository import SQLGenreRepository
from app.schema.genre_schema import GenreCreate, GenreRead, GenreUpdate


class GenreService:
    def __init__(self, db: Session):
        self.repo = SQLGenreRepository(db)
        self.db = db

    def get(self, genre_id: int) -> GenreRead | None:
        obj = self.repo.get(genre_id)
        return GenreRead.model_validate(obj) if obj else None

    def list(
        self, offset: int, limit: int, search: str | None
    ) -> tuple[list[GenreRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [GenreRead.model_validate(r) for r in rows], total

    def create(self, payload: GenreCreate) -> GenreRead:
        if self.repo.get_by_name(payload.name):
            raise ValueError("Genre with this name already exists")

        obj = Genre(**payload.model_dump())
        obj = self.repo.create(obj)
        self.db.commit()
        self.db.refresh(obj)
        return GenreRead.model_validate(obj)

    def update(self, genre_id: int, payload: GenreUpdate) -> GenreRead | None:
        obj = self.repo.get(genre_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing = self.repo.get_by_name(update_data["name"])
            if existing and existing.id != genre_id:
                raise ValueError("Genre with this name already exists")

        for key, value in update_data.items():
            setattr(obj, key, value)

        obj = self.repo.update(obj)
        self.db.commit()
        self.db.refresh(obj)
        return GenreRead.model_validate(obj)

    def delete(self, genre_id: int) -> bool:
        obj = self.repo.get(genre_id)
        if not obj:
            return False
        self.repo.delete(obj)
        self.db.commit()
        return True
