from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.mechanic_model import Mechanic
from app.repository.mechanic.i_mechanic_repository import IMechanicRepository


class MechanicRepositorySQL(IMechanicRepository):
    def __init__(self, db: Session):
        self.db = db

    def get(self, mechanic_id: int) -> Mechanic | None:
        return self.db.get(Mechanic, int(mechanic_id))

    def get_by_name(self, name: str) -> Mechanic | None:
        stmt = select(Mechanic).where(Mechanic.name == name)
        return self.db.execute(stmt).scalars().first()

    def list(
        self,
        offset: int,
        limit: int,
        search: str | None,
        sort_by: str | None,
        sort_order: str | None = "asc",
    ) -> tuple[list[Mechanic], int]:
        stmt = select(Mechanic)

        if search:
            stmt = stmt.where(Mechanic.name.ilike(f"%{search}%"))

        # whitelist sorting
        if sort_by == "name" or not sort_by:
            col = Mechanic.name
            stmt = stmt.order_by(
                col.asc() if (sort_order or "asc") == "asc" else col.desc()
            )
        else:
            stmt = stmt.order_by(Mechanic.name.asc())

        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = (
            self.db.execute(stmt.offset(int(offset)).limit(int(limit))).scalars().all()
        )
        return rows, total

    def create(self, mechanic_data: dict) -> Mechanic:
        obj = Mechanic(**mechanic_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, mechanic_id: int, mechanic_data: dict) -> Mechanic | None:
        obj = self.get(mechanic_id)
        if not obj:
            return None

        for k, v in mechanic_data.items():
            setattr(obj, k, v)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, mechanic_id: int) -> bool:
        obj = self.get(mechanic_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
