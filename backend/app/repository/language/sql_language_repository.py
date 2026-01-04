from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.language_model import Language
from app.repository.language.i_language_repository import ILanguageRepository


class LanguageRepositorySQL(ILanguageRepository):
    def __init__(self, db: Session):
        self.db = db

    def get(self, language_id: int) -> Language | None:
        return self.db.get(Language, int(language_id))

    def get_by_name(self, name: str) -> Language | None:
        stmt = select(Language).where(Language.language == name)
        return self.db.execute(stmt).scalars().first()

    def list(self, offset: int, limit: int, search: str | None):
        stmt = select(Language)
        if search:
            stmt = stmt.where(Language.language.ilike(f"%{search}%"))

        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()

        rows = (
            self.db.execute(
                stmt.order_by(Language.id.desc()).offset(offset).limit(limit)
            )
            .scalars()
            .all()
        )
        return rows, total

    def create(self, language_data: dict) -> Language:
        obj = Language(**language_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, language_id: int, language_data: dict) -> Language | None:
        obj = self.get(language_id)
        if not obj:
            return None

        for k, v in language_data.items():
            setattr(obj, k, v)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, language_id: int) -> bool:
        obj = self.get(language_id)
        if not obj:
            return False

        self.db.delete(obj)
        self.db.commit()
        return True
