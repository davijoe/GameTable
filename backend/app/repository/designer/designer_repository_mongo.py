from app.repository.designer.i_designer_repository import IDesignerRepository
from pymongo.collection import Collection


class DesignerRepositoryMongo(IDesignerRepository):
    def __init__(self, db):
        self.games: Collection = db["games"]

    def _doc(self, doc: dict | None):
        if not doc:
            return None
        doc["id"] = doc.get("id", doc.get("_id"))
        return doc

    def get(self, designer_id: int):
        pid = int(designer_id)

        pipeline = [
            {"$match": {"designers.id": pid}},
            {"$unwind": "$designers"},
            {"$match": {"designers.id": pid}},
            {"$replaceRoot": {"newRoot": "$designers"}},
            {"$limit": 1},
        ]

        docs = list(self.games.aggregate(pipeline))
        if not docs:
            return None

        doc = docs[0]
        doc["id"] = int(doc["id"])
        return doc

    def get_by_name(self, name: str):
        # Case-insensitive exact-ish match
        pipeline = [
            {"$match": {"designers.name": {"$regex": f"^{name}$", "$options": "i"}}},
            {"$unwind": "$designers"},
            {"$match": {"designers.name": {"$regex": f"^{name}$", "$options": "i"}}},
            {"$replaceRoot": {"newRoot": "$designers"}},
            {"$limit": 1},
        ]

        docs = list(self.games.aggregate(pipeline))
        if not docs:
            return None

        doc = docs[0]
        doc["id"] = int(doc["id"])
        return doc

    def list(
		self,
		offset: int,
		limit: int,
		search: str | None,
		sort_order: str | None = "asc",
    ):
        sort_dir = 1 if (sort_order or "asc") == "asc" else -1

        match_stage = {}
        if search:
            match_stage["designers.name"] = {
				"$regex": search,
				"$options": "i",
			}

        count_pipeline = [
			{"$unwind": "$artists"},
			{"$match": match_stage} if match_stage else {"$match": {}},
			{"$count": "total"},
		]

        count_result = list(self.games.aggregate(count_pipeline))
        total = count_result[0]["total"] if count_result else 0

        pipeline = [
			{"$unwind": "$artists"},
			{"$match": match_stage} if match_stage else {"$match": {}},
			{"$sort": {"artists.name": sort_dir}},
			{"$skip": offset},
			{"$limit": limit},
			{"$replaceRoot": {"newRoot": "$artists"}},
		]

        docs = list(self.games.aggregate(pipeline))
        return [self._doc(d) for d in docs], total

    def create(self, designer_data: dict):
        doc = dict(designer_data)

        # if your payload already includes id, keep it; otherwise you must decide an id strategy
        if "id" not in doc and "_id" not in doc:
            raise ValueError(
                "Mongo designer create requires an integer 'id' field for backend switching."
            )

        res = self.col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return self._doc(doc)

    def update(self, designer_id: int, designer_data: dict):
        res = self.col.update_one(
            {"id": int(designer_id)}, {"$set": dict(designer_data)}
        )
        if res.matched_count == 0:
            return None
        return self.get(designer_id)

    def delete(self, designer_id: int) -> bool:
        res = self.col.delete_one({"id": int(designer_id)})
        return res.deleted_count == 1
