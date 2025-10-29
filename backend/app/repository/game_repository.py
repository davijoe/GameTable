from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.model.game_model import Game


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, game_id: int) -> Optional[Game]:
        return self.db.get(Game, game_id)

    def list(
        self, offset: int = 0, limit: int = 50, search: Optional[str] = None
    ) -> Tuple[List[Game], int]:
        stmt = select(Game)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(Game.name.ilike(like))
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, g: Game) -> Game:
        self.db.add(g)
        self.db.flush()
        return g

    def delete(self, game_id: int) -> bool:
        obj = self.get(game_id)
        if not obj:
            return False
        self.db.delete(obj)
        return True
