from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.model.game_model import Game
from app.repository.game.i_game_repository import IGameRepository


class GameRepositorySQL(IGameRepository):
    SORT_FIELDS = {
        "bgg_rating": Game.bgg_rating.desc(),
        "year_published": Game.year_published.desc(),
        "playing_time": Game.playing_time.asc(),
        "name": Game.name.asc(),
    }

    def __init__(self, db):
        self.db = db

    def get(self, game_id):
        return self.db.get(Game, game_id)

    def list(self, offset, limit, search, sort_by, sort_order = "desc"):
        stmt = select(Game)

        if search:
            stmt = stmt.where(Game.name.ilike(f"%{search}%"))

        if sort_by in self.SORT_FIELDS:
            col = getattr(Game, sort_by)
            stmt = stmt.order_by(col.asc() if sort_order == "desc" else col.desc())

        total = self.db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
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
        obj = self.get(game_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

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
