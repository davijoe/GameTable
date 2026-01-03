from typing import Any

from pymongo.collection import Collection

from app.repository.video.i_video_repository import IVideoRepository


class VideoRepositoryMongo(IVideoRepository):
    def __init__(self, db):
        self.col: Collection = db["videos"]

    def get(self, video_id: Any):
        doc = self.col.find_one({"_id": int(video_id)})
        if not doc:
            return None
        doc["id"] = doc["_id"]
        return doc

    def list(
        self,
        offset: int,
        limit: int,
        search: str | None,
        sort_by: str | None,
        sort_order: str | None = None,
    ):
        query = {}
        if search:
            query["title"] = {"$regex": search, "$options": "i"}

        total = self.col.count_documents(query)

        sort_field = "title"
        sort_dir = 1 if (sort_order or "asc") == "asc" else -1

        cursor = (
            self.col.find(query).skip(offset).limit(limit).sort(sort_field, sort_dir)
        )

        items = []
        for d in cursor:
            d["id"] = d["_id"]
            items.append(d)

        return items, total

    def create(self, video_data: dict):
        doc = dict(video_data)
        res = self.col.insert_one(doc)
        doc["_id"] = res.inserted_id
        doc["id"] = doc["_id"]
        return doc

    def update(self, video_id: Any, video_data: dict):
        res = self.col.update_one({"_id": int(video_id)}, {"$set": dict(video_data)})
        if res.matched_count == 0:
            return None
        return self.get(video_id)

    def delete(self, video_id: Any) -> bool:
        res = self.col.delete_one({"_id": int(video_id)})
        return res.deleted_count == 1
