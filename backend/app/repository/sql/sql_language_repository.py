from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.language_model import Language


class SQLLanguageRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, language_id: int) -> Language | None:
        return self.db.get(Language, language_id)

    def get_by_name(self, language: str) -> Language | None:
        return self.db.execute(
            select(Language).where(Language.language == language)
        ).scalar_one_or_none()

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[Language], int]:
        stmt = select(Language)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(Language.language.ilike(like))
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, language: Language) -> Language:
        self.db.add(language)
        self.db.commit()
        self.db.refresh(language)
        return language

    def update(self, language: Language) -> Language:
        self.db.merge(language)
        self.db.commit()
        self.db.refresh(language)
        return language

    def delete(self, language: Language) -> bool:
        try:
            if not language:
                return False
            
            if language.videos:
                raise ValueError(f"Cannot delete language with id {language.id}: it has associated videos")
            
            self.db.delete(language)
            self.db.commit()
            return True
        except ValueError:
            self.db.rollback()
            raise
        except Exception:
            self.db.rollback()
            raise
