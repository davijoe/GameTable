from datetime import date, datetime
from typing import Any

from pymongo.collection import Collection

from app.repository.artist.i_artist_repository import IArtistRepository
from app.schema.artist_schema import ArtistCreate, ArtistRead, ArtistUpdate


class ArtistRepositoryMongo(IArtistRepository):
    def __init__(self, db):
        self.games: Collection = db["games"]

    def _convert_dates(self, doc: dict) -> dict:
        for k, v in doc.items():
            if isinstance(v, date) and not isinstance(v, datetime):
                doc[k] = datetime(v.year, v.month, v.day)
        return doc

    def _doc(self, doc: dict | None):
        if not doc:
            return None
        doc["id"] = doc.get("id", doc.get("_id"))
        return doc

    def get(self, artist_id: int):
        pid = int(artist_id)

        pipeline = [
            {"$match": {"artists.id": pid}},
            {"$unwind": "$artists"},
            {"$match": {"artists.id": pid}},
            {"$replaceRoot": {"newRoot": "$artists"}},
            {"$limit": 1},
        ]

        docs = list(self.games.aggregate(pipeline))
        if not docs:
            return None

        doc = docs[0]
        doc["id"] = int(doc["id"])
        return doc

    def get_by_name(self, name: str):
        pipeline = [
            {"$match": {"artists.name": {"$regex": f"^{name}$", "$options": "i"}}},
            {"$unwind": "$artists"},
            {"$match": {"artists.name": {"$regex": f"^{name}$", "$options": "i"}}},
            {"$replaceRoot": {"newRoot": "$artists"}},
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
            match_stage["artists.name"] = {
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

    def create(self, artist_data: ArtistCreate | dict) -> ArtistRead:
        doc = self._convert_dates(artist_data)

        res = self.col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return self._doc_to_artist(doc)

    def update(
        self, artist_id: Any, artist_data: ArtistUpdate | dict
    ) -> ArtistRead | None:
        update_doc = self._convert_dates(artist_id)

        res = self.col.update_one({"_id": artist_id}, {"$set": update_doc})
        if res.matched_count == 0:
            return None
        return self.get(artist_id)

    def delete(self, artist_id: Any) -> bool:
        res = self.col.delete_one({"_id": artist_id})
        return res.deleted_count == 1
