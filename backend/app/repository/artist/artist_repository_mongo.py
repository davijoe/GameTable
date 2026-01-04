from typing import Any
from datetime import datetime, date

from pymongo.collection import Collection

from app.repository.artist.i_artist_repository import IArtistRepository
from app.schema.artist_schema import ArtistCreate, ArtistRead, ArtistUpdate


class ArtistRepositoryMongo(IArtistRepository):
	def __init__(self, db):
		self.col: Collection = db["artists"]

	def _convert_dates(self, doc: dict) -> dict:
		for k, v in doc.items():
			if isinstance(v, date) and not isinstance(v, datetime):
				doc[k] = datetime(v.year, v.month, v.day)
		return doc

	def _doc_to_artist(self, doc: dict) -> ArtistRead | None:
		if not doc:
			return None
		doc["id"] = str(doc.get("_id"))
		return ArtistRead(**doc)

	def get(self, artist_id: Any) -> ArtistRead | None:
		doc = self.col.find_one({"_id": artist_id})
		return self._doc_to_artist(doc)

	def get_by_name(self, name: str) -> ArtistRead | None:
		doc = self.col.find_one({"name": name})
		return self._doc_to_artist(doc)

	def list(
		self,
		offset: int,
		limit: int,
		search: str | None = None,
	) -> tuple[list[ArtistRead], int]:
		query = {}
		if search:
			query["name"] = {"$regex": search, "$options": "i"}

		total = self.col.count_documents(query)
		cursor = (
			self.col.find(query)
			.skip(offset)
			.limit(limit)
			.sort("name", 1)
		)

		return [self._doc_to_artist(d) for d in cursor], total

	def create(self, artist_data: ArtistCreate | dict) -> ArtistRead:
		#convert Pydantic or dict to Mongo-ready dict
		if hasattr(artist_data, "model_dump"):
			doc = artist_data.model_dump(exclude_unset=True)
		elif hasattr(artist_data, "__dict__"):
			doc = {k: v for k, v in artist_data.__dict__.items() if not k.startswith("_")}
		elif isinstance(artist_data, dict):
			doc = artist_data
		else:
			raise TypeError(f"Unsupported type for artist_data: {type(artist_data)}")

		doc = self._convert_dates(doc)

		res = self.col.insert_one(doc)
		doc["_id"] = res.inserted_id
		return self._doc_to_artist(doc)

	def update(self, artist_id: Any, artist_data: ArtistUpdate | dict) -> ArtistRead | None:
		if hasattr(artist_data, "model_dump"):
			update_doc = artist_data.model_dump(exclude_unset=True)
		elif hasattr(artist_data, "__dict__"):
			update_doc = {k: v for k, v in artist_data.__dict__.items() if not k.startswith("_")}
		elif isinstance(artist_data, dict):
			update_doc = artist_data
		else:
			raise TypeError(f"Unsupported type for artist_data: {type(artist_data)}")

		update_doc = self._convert_dates(update_doc)

		res = self.col.update_one({"_id": artist_id}, {"$set": update_doc})
		if res.matched_count == 0:
			return None
		return self.get(artist_id)

	def delete(self, artist_id: Any) -> bool:
		res = self.col.delete_one({"_id": artist_id})
		return res.deleted_count == 1
