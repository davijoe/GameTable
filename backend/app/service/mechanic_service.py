from sqlalchemy.orm import Session

from app.model.mechanic_model import Mechanic
from app.repository.mechanic.sql_mechanic_repository import SQLMechanicRepository
from app.schema.mechanic_schema import MechanicCreate, MechanicRead, MechanicUpdate


class MechanicService:
    def __init__(self, db: Session):
        self.repo = SQLMechanicRepository(db)
        self.db = db

    def get(self, mechanic_id: int) -> MechanicRead | None:
        obj = self.repo.get(mechanic_id)
        return MechanicRead.model_validate(obj) if obj else None

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[MechanicRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [MechanicRead.model_validate(r) for r in rows], total

    def create(self, payload: MechanicCreate) -> MechanicRead:
        if self.repo.get_by_name(payload.name):
            raise ValueError("Mechanic with this name already exists")

        obj = Mechanic(**payload.model_dump())
        obj = self.repo.create(obj)
        self.db.commit()
        self.db.refresh(obj)
        return MechanicRead.model_validate(obj)

    def update(self, mechanic_id: int, payload: MechanicUpdate) -> MechanicRead | None:
        obj = self.repo.get(mechanic_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing = self.repo.get_by_name(update_data["name"])
            if existing and existing.id != mechanic_id:
                raise ValueError("Mechanic with this name already exists")

        for key, value in update_data.items():
            setattr(obj, key, value)

        obj = self.repo.update(obj)
        self.db.commit()
        self.db.refresh(obj)
        return MechanicRead.model_validate(obj)

    def delete(self, mechanic_id: int) -> bool:
        obj = self.repo.get(mechanic_id)
        if not obj:
            return False
        self.repo.delete(obj)
        self.db.commit()
        return True
