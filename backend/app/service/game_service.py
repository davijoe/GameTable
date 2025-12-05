#from typing import List, Optional, Tuple

#from sqlalchemy.orm import Session

#from app.model.game_model import Game
from app.schema.game_schema import GameCreate, GameRead, GameUpdate
from app.repository.game.game_repository_factory import get_game_repository

class GameService:
	def __init__(self):
		self.repo = get_game_repository()

	def list(self, offset, limit, search):
		rows, total = self.repo.list(offset, limit, search)
		return [GameRead.model_validate(r) for r in rows], total

	def get(self, game_id):
		obj = self.repo.get(game_id)
		return GameRead.model_validate(obj) if obj else None

	def create(self, payload: GameCreate):
		return GameRead.model_validate(self.repo.create(payload.model_dump()))

	def update(self, game_id, payload: GameUpdate):
		obj = self.repo.update(game_id, payload.model_dump(exclude_unset=True))
		return GameRead.model_validate(obj) if obj else None

	def delete(self, game_id):
		return self.repo.delete(game_id)

#old service before new setup - might want to look at
'''
class GameService:
    def __init__(self, db: Session):
        self.repo = SQLGameRepository(db)
        self.db = db

    def get(self, game_id: int) -> Optional[GameRead]:
        obj = self.repo.get(game_id)
        return GameRead.model_validate(obj) if obj else None

    def list(
        self, offset: int, limit: int, search: Optional[str]
    ) -> Tuple[List[GameRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [GameRead.model_validate(r) for r in rows], total

    def create(self, payload: GameCreate) -> GameRead:
        obj = Game(**payload.model_dump())
        obj = self.repo.create(obj)
        self.db.commit()
        self.db.refresh(obj)
        return GameRead.model_validate(obj)

    def update(self, game_id: int, payload: GameUpdate) -> Optional[GameRead]:
        obj = self.repo.get(game_id)
        if not obj:
            return None
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return GameRead.model_validate(obj)

    def delete(self, game_id: int) -> bool:
        ok = self.repo.delete(game_id)
        if ok:
            self.db.commit()
        return ok
'''