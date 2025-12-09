from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.designer_model import Designer


class SQLDesignerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, designer_id: int) -> Designer | None:
        return self.db.get(Designer, designer_id)

    def get_by_name(self, name: str) -> Designer | None:
        return self.db.execute(
            select(Designer).where(Designer.name == name)
        ).scalar_one_or_none()

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[Designer], int]:
        stmt = select(Designer)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(Designer.name.ilike(like))
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, designer: Designer) -> Designer:
        self.db.add(designer)
        self.db.commit()
        return designer

    def update(self, designer: Designer) -> Designer:
        self.db.merge(designer)
        self.db.commit()
        return designer

    def delete(self, designer: Designer) -> None:
        self.db.delete(designer)
        self.db.commit()
