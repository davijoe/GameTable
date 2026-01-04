from pymongo.collection import Collection

from app.repository.review.i_review_repository import IReviewRepository


class ReviewRepositoryMongo(IReviewRepository):
    def __init__(self, db):
        self.col: Collection = db["reviews"]

    def _doc(self, doc: dict | None):
        if not doc:
            return None
        doc["id"] = doc.get("id", doc.get("_id"))
        return doc

    def get(self, review_id: int):
        doc = self.col.find_one({"id": int(review_id)}) or self.col.find_one(
            {"_id": int(review_id)}
        )
        return self._doc(doc)

    def get_review_count_for_game(self, game_id: int) -> int:
        return self.col.count_documents({"game_id": int(game_id)})

    def list_by_game(self, game_id: int, offset: int, limit: int):
        query = {"game_id": int(game_id)}
        total = self.col.count_documents(query)
        cursor = self.col.find(query).skip(offset).limit(limit).sort("id", -1)
        return [self._doc(d) for d in cursor], total

    def list(self, offset: int, limit: int, search: str | None):
        query = {}
        if search:
            query["comment"] = {"$regex": search, "$options": "i"}
        total = self.col.count_documents(query)
        cursor = self.col.find(query).skip(offset).limit(limit).sort("id", -1)
        return [self._doc(d) for d in cursor], total

    def create(self, review_data: dict):
        doc = dict(review_data)

        # requires an id strategy if you want int ids everywhere
        if "id" not in doc and "_id" not in doc:
            raise ValueError(
                "Mongo review create requires integer 'id' for backend switching."
            )

        res = self.col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return self._doc(doc)

    def update(self, review_id: int, review_data: dict):
        res = self.col.update_one({"id": int(review_id)}, {"$set": dict(review_data)})
        if res.matched_count == 0:
            return None
        return self.get(review_id)

    def delete(self, review_id: int) -> bool:
        res = self.col.delete_one({"id": int(review_id)})
        return res.deleted_count == 1
