from typing import Any

from pymongo.collection import Collection

from app.repository.game.i_game_repository import IGameRepository
from app.schema.game_schema import GameCreate, GameRead, GameUpdate


class GameRepositoryMongo(IGameRepository):
    SORT_FIELDS = {
        "bgg_rating": "bgg_rating",
        "year_published": "year_published",
        "playing_time": "playing_time",
        "name": "name",
    }

    def __init__(self, db):
        self.col: Collection = db["games"]

    def _doc_to_game(self, doc: dict) -> GameRead:
        if not doc:
            return None
        doc["id"] = doc["_id"]
        images = doc.get("images") or {}
        doc["thumbnail"] = images.get("thumbnail")
        doc["image"] = images.get("image")
        return GameRead(**doc)

    def get(self, game_id: Any) -> GameRead | None:
        # casting to int is apparently important
        doc = self.col.find_one({"_id": int(game_id)})
        return self._doc_to_game(doc)

    def list(
        self,
        offset: int,
        limit: int,
        search: str | None = None,
        sort_by: str | None = None,
        sort_order: str = "desc",
    ) -> tuple[list[dict], int]:
        query = {}
        if search:
            query["name"] = {"$regex": search, "$options": "i"}

        total = self.col.count_documents(query)
        cursor = self.col.find(query).skip(offset).limit(limit)

        if sort_by in self.SORT_FIELDS:
            sort_field = self.SORT_FIELDS[sort_by]
            pymongo_order = -1 if sort_order == "desc" else 1
            cursor = cursor.sort(sort_field, pymongo_order)

        return [self._doc_to_game(d) for d in cursor], total

    def create(self, game_data: GameCreate) -> GameRead:
        doc = game_data.model_dump(exclude_unset=True)
        result = self.col.insert_one(doc)
        doc["_id"] = result.inserted_id
        return self._doc_to_game(doc)

    def update(self, game_id: Any, game_data: GameUpdate) -> GameRead | None:
        update_doc = game_data.model_dump(exclude_unset=True)
        res = self.col.update_one({"_id": game_id}, {"$set": update_doc})
        if res.matched_count == 0:
            return None
        return self.get(game_id)

    def delete(self, game_id: Any) -> bool:
        res = self.col.delete_one({"_id": game_id})
        return res.deleted_count == 1

