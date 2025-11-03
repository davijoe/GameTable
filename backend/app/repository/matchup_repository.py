from typing import List, Optional, Tuple

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.matchup_model import Matchup


class MatchupRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, matchup_id: int) -> Optional[Matchup]:
        return self.db.get(Matchup, matchup_id)

    def list(
        self, offset: int = 0, limit: int = 50, game_id: Optional[int] = None
    ) -> Tuple[List[Matchup], int]:
        stmt = select(Matchup)
        if game_id:
            stmt = stmt.where(Matchup.game_id == game_id)
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, matchup: Matchup) -> Matchup:
        self.db.add(matchup)
        self.db.flush()
        return matchup

    def update(self, matchup: Matchup) -> Matchup:
        self.db.merge(matchup)
        self.db.flush()
        return matchup

    def delete(self, matchup: Matchup) -> None:
        self.db.delete(matchup)
        self.db.flush()

    def get_user_matchups(
        self, user_id: int, offset: int = 0, limit: int = 50
    ) -> Tuple[List[Matchup], int]:
        stmt = select(Matchup).where(
            (Matchup.user_id_1 == user_id) | (Matchup.user_id_2 == user_id)
        )
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

