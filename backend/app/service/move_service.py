from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.model.move_model import Move
from app.repository.move_repository import MoveRepository
from app.schema.move_schema import MoveCreate, MoveRead, MoveUpdate


class MoveService:
    def __init__(self, db: Session):
        self.repo = MoveRepository(db)
        self.db = db

    def get(self, move_id: int) -> Optional[MoveRead]:
        obj = self.repo.get(move_id)
        return MoveRead.model_validate(obj) if obj else None

    def list(
        self, offset: int, limit: int, ply: Optional[int] = None
    ) -> Tuple[List[MoveRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, ply=ply)
        return [MoveRead.model_validate(r) for r in rows], total

    def create(self, payload: MoveCreate) -> MoveRead:
        obj = Move(**payload.model_dump())
        obj = self.repo.create(obj)
        self.db.commit()
        self.db.refresh(obj)
        return MoveRead.model_validate(obj)

    def update(self, move_id: int, payload: MoveUpdate) -> Optional[MoveRead]:
        obj = self.repo.get(move_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)

        obj = self.repo.update(obj)
        self.db.commit()
        self.db.refresh(obj)
        return MoveRead.model_validate(obj)

    def delete(self, move_id: int) -> bool:
        obj = self.repo.get(move_id)
        if not obj:
            return False
        self.repo.delete(obj)
        self.db.commit()
        return True

