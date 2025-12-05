from typing import Any, Tuple, List
from pymongo.collection import Collection
from app.repository.game.i_game_repository import IGameRepository

def _doc_to_game_dict(doc: dict) -> dict:
    if not doc:
        print("error in _doc_to_game_dict")
        return None

    return {
        "id": doc.get("_id"),
        "name": doc.get("name"),
        "slug": doc.get("slug"),
        "year_published": doc.get("year_published"),
        "ratings": doc.get("ratings", {}),
        "description": doc.get("description"),
        "playing_time": doc.get("playing_time"),
        "player_count_min": doc.get("player_count", {}).get("min") if doc.get("player_count") else None,
        "player_count_max": doc.get("player_count", {}).get("max") if doc.get("player_count") else None,
        "minimum_age": doc.get("minimum_age"),
        "thumbnail": doc.get("images", {}).get("thumbnail"),
        "image": doc.get("images", {}).get("image"),
        "designers": doc.get("designers", []),
        "artists": doc.get("artists", []),
        "genres": doc.get("genres", []),
        "publishers": doc.get("publishers", []),
        "mechanics": doc.get("mechanics", []),
        "videos": doc.get("videos", []),
    }
class GameRepositoryMongo(IGameRepository):
    def __init__(self, db):
        # db is a pymongo.database.Database
        self.db = db
        self.col: Collection = db["games"]

    def get(self, game_id: Any):
        # migration set _id to original id (int). Use that.
        doc = self.col.find_one({"_id": game_id})
        return _doc_to_game_dict(doc)

    def list(self, offset: int, limit: int, search: str | None) -> Tuple[List[dict], int]:
        query = {}
        if search:
            # case-insensitive search on name
            query["name"] = {"$regex": search, "$options": "i"}

        total = self.col.count_documents(query)
        cursor = self.col.find(query).skip(offset).limit(limit).sort("name", 1)
        docs = list(cursor)
        rows = [_doc_to_game_dict(d) for d in docs]
        return rows, total

    def create(self, game_data: dict):
        # Expect game_data to be a mapping similar to GameCreate.model_dump()
        # Choose an _id strategy: if the incoming dict has id, use it; otherwise let Mongo create ObjectId
        doc = dict(game_data)
        if "id" in doc:
            doc["_id"] = doc.pop("id")
        # convert nested fields to migration-like shape if needed; simple approach:
        # put images back into images.* if incoming uses thumbnail/image keys
        images = {}
        if "thumbnail" in doc:
            images["thumbnail"] = doc.pop("thumbnail")
        if "image" in doc:
            images["image"] = doc.pop("image")
        if images:
            doc.setdefault("images", {}).update(images)

        result = self.col.insert_one(doc)
        new_doc = self.col.find_one({"_id": doc.get("_id", result.inserted_id)})
        return _doc_to_game_dict(new_doc)

    def update(self, game_id: Any, game_data: dict):
        if not game_data:
            return self.get(game_id)

        # Map incoming game_data keys to fields in Mongo. For simplicity, apply $set to top-level keys.
        # If nested updates required (e.g. images.thumbnail), caller should pass nested keys or we can translate common ones:
        update_doc = {}

        # translate possible image keys back into images.* path
        if "thumbnail" in game_data or "image" in game_data:
            img_update = {}
            if "thumbnail" in game_data:
                img_update["images.thumbnail"] = game_data.pop("thumbnail")
            if "image" in game_data:
                img_update["images.image"] = game_data.pop("image")
            update_doc.update(img_update)

        # remaining top-level fields go straight to set
        for k, v in game_data.items():
            update_doc[k] = v

        # Build $set with flattened keys
        set_payload = {}
        for k, v in update_doc.items():
            # if key already contains dot path (like images.thumbnail) keep it, else set top-level
            set_payload[k] = v

        res = self.col.update_one({"_id": game_id}, {"$set": set_payload})
        if res.matched_count == 0:
            return None
        return self.get(game_id)

    def delete(self, game_id: Any) -> bool:
        res = self.col.delete_one({"_id": game_id})
        return res.deleted_count == 1

