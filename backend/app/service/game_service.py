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
