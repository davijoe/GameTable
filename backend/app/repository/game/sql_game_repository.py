from pytest import Session
from sqlalchemy import func, select
from app.repository.game.i_game_repository import IGameRepository
from app.model.game_model import Game


class GameRepositorySQL(IGameRepository):
	def __init__(self, db: Session):
		self.db = db

	def get(self, game_id):
		return self.db.get(Game, game_id)

	def list(self, offset, limit, search):
		stmt = select(Game)
		if search:
			stmt = stmt.where(Game.name.ilike(f"%{search}%"))

		total = self.db.execute(
			select(func.count()).select_from(stmt.subquery())
		).scalar_one()

		rows = (
			self.db.execute(stmt.offset(offset).limit(limit))
			.scalars()
			.all()
		)

		return rows, total

	def create(self, game_data):
		obj = Game(**game_data)
		self.db.add(obj)
		self.db.commit()
		self.db.refresh(obj)
		return obj

	def update(self, game_id, game_data):
		obj = self.get(game_id)
		if not obj:
			return None

		for k, v in game_data.items():
			setattr(obj, k, v)

		self.db.commit()
		self.db.refresh(obj)
		return obj

	def delete(self, game_id):
		obj = self.get(game_id)
		if not obj:
			return False
		self.db.delete(obj)
		self.db.commit()
		return True
	