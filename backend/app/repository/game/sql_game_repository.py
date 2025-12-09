from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.model.game_model import Game
from app.repository.game.i_game_repository import IGameRepository


class GameRepositorySQL(IGameRepository):
    def __init__(self, db):
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

        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()

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
        try:
            obj = self.get(game_id)
            if not obj:
                return False
            
            for review in obj.reviews:
                self.db.delete(review)
            
            for video in obj.videos:
                self.db.delete(video)
            
            obj.artists.clear()
            obj.designers.clear()
            obj.publishers.clear()
            obj.mechanics.clear()
            obj.genres.clear()
            
            self.db.delete(obj)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise

    def get_detail(self, game_id):
        stmt = (
            select(Game)
            .options(
                selectinload(Game.artists),
                selectinload(Game.designers),
                selectinload(Game.publishers),
                selectinload(Game.mechanics),
            )
            .where(Game.id == game_id)
        )
        return self.db.execute(stmt).scalars().first()
