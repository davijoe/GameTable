from datetime import datetime
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.model.matchup_model import Matchup
from app.repository.matchup_repository import MatchupRepository
from app.schema.matchup_schema import MatchupCreate, MatchupRead, MatchupUpdate


class MatchupService:
    def __init__(self, db: Session):
        self.repo = MatchupRepository(db)
        self.db = db

    def get(self, matchup_id: int) -> Optional[MatchupRead]:
        obj = self.repo.get(matchup_id)
        return MatchupRead.model_validate(obj) if obj else None

    def list(
        self, offset: int, limit: int, game_id: Optional[int] = None
    ) -> Tuple[List[MatchupRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, game_id=game_id)
        return [MatchupRead.model_validate(r) for r in rows], total

    def create(self, payload: MatchupCreate) -> MatchupRead:
        data = payload.model_dump()
        data["created_at"] = datetime.now().date()
        obj = Matchup(**data)
        obj = self.repo.create(obj)
        self.db.commit()
        self.db.refresh(obj)
        return MatchupRead.model_validate(obj)

    def update(self, matchup_id: int, payload: MatchupUpdate) -> Optional[MatchupRead]:
        obj = self.repo.get(matchup_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)

        obj = self.repo.update(obj)
        self.db.commit()
        self.db.refresh(obj)
        return MatchupRead.model_validate(obj)

    def delete(self, matchup_id: int) -> bool:
        obj = self.repo.get(matchup_id)
        if not obj:
            return False
        self.repo.delete(obj)
        self.db.commit()
        return True

    def get_user_matchups(
        self, user_id: int, offset: int, limit: int
    ) -> Tuple[List[MatchupRead], int]:
        rows, total = self.repo.get_user_matchups(
            user_id=user_id, offset=offset, limit=limit
        )
        return [MatchupRead.model_validate(r) for r in rows], total

