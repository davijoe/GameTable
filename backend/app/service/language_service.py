from sqlalchemy.orm import Session

from app.model.language_model import Language
from app.repository.sql.sql_language_repository import SQLLanguageRepository
from app.schema.language_schema import LanguageCreate, LanguageRead, LanguageUpdate


class LanguageService:
    def __init__(self, db: Session):
        self.repo = SQLLanguageRepository(db)
        self.db = db

    def get(self, language_id: int) -> LanguageRead | None:
        obj = self.repo.get(language_id)
        return LanguageRead.model_validate(obj) if obj else None

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[LanguageRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [LanguageRead.model_validate(r) for r in rows], total

    def create(self, payload: LanguageCreate) -> LanguageRead:
        if self.repo.get_by_name(payload.language):
            raise ValueError("Language with this name already exists")

        language = Language(**payload.model_dump())
        language = self.repo.create(language)
        self.db.commit()
        self.db.refresh(language)
        return LanguageRead.model_validate(language)

    def update(self, language_id: int, payload: LanguageUpdate) -> LanguageRead | None:
        obj = self.repo.get(language_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)

        if "language" in update_data:
            existing = self.repo.get_by_name(update_data["language"])
            if existing and existing.id != language_id:
                raise ValueError("Language with this name already exists")

        for key, value in update_data.items():
            setattr(obj, key, value)

        obj = self.repo.update(obj)
        self.db.commit()
        self.db.refresh(obj)
        return LanguageRead.model_validate(obj)

    def delete(self, language_id: int) -> bool:
        obj = self.repo.get(language_id)
        if not obj:
            return False
        self.repo.delete(obj)
        self.db.commit()
        return True
