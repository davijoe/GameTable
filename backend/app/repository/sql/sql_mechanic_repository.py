from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.mechanic_model import Mechanic


class SQLMechanicRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, mechanic_id: int) -> Mechanic | None:
        return self.db.get(Mechanic, mechanic_id)

    def get_by_name(self, name: str) -> Mechanic | None:
        return self.db.execute(select(Mechanic).where(Mechanic.name == name)).scalar_one_or_none()

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[Mechanic], int]:
        stmt = select(Mechanic)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(Mechanic.name.ilike(like))
        total = self.db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, mechanic: Mechanic) -> Mechanic:
        self.db.add(mechanic)
        self.db.flush()
        return mechanic

    def update(self, mechanic: Mechanic) -> Mechanic:
        self.db.merge(mechanic)
        self.db.flush()
        return mechanic

    def delete(self, mechanic: Mechanic) -> None:
        self.db.delete(mechanic)
        self.db.flush()
