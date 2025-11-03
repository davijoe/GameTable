from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.move_model import Move


class MoveRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, move_id: int) -> Optional[Move]:
        return self.db.get(Move, move_id)

    def list(
        self, offset: int = 0, limit: int = 50, ply: Optional[int] = None
    ) -> Tuple[List[Move], int]:
        stmt = select(Move)
        if ply is not None:
            stmt = stmt.where(Move.ply == ply)
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, move: Move) -> Move:
        self.db.add(move)
        self.db.flush()
        return move

    def update(self, move: Move) -> Move:
        self.db.merge(move)
        self.db.flush()
        return move

    def delete(self, move: Move) -> None:
        self.db.delete(move)
        self.db.flush()

