from pymongo.collection import Collection

from app.repository.publisher.i_publisher_repository import IPublisherRepository


class PublisherRepositoryMongo(IPublisherRepository):
    def __init__(self, db):
        self.col: Collection = db["publishers"]

    def _doc(self, doc: dict | None):
        if not doc:
            return None
        doc["id"] = doc.get("id", doc.get("_id"))
        return doc

    def get(self, publisher_id: int):
        doc = self.col.find_one({"id": int(publisher_id)}) or self.col.find_one(
            {"_id": int(publisher_id)}
        )
        return self._doc(doc)

    def get_by_name(self, name: str):
        doc = self.col.find_one({"name": name})
        return self._doc(doc)

    def list(
        self,
        offset: int,
        limit: int,
        search: str | None,
        sort_by: str | None,
        sort_order: str | None = "asc",
    ):
        query = {}
        if search:
            query["name"] = {"$regex": search, "$options": "i"}

        total = self.col.count_documents(query)
        sort_dir = 1 if (sort_order or "asc") == "asc" else -1
        cursor = self.col.find(query).skip(offset).limit(limit).sort("name", sort_dir)

        return [self._doc(d) for d in cursor], total

    def create(self, publisher_data: dict):
        doc = dict(publisher_data)

        # if your payload already includes id, keep it; otherwise you must decide an id strategy
        if "id" not in doc and "_id" not in doc:
            raise ValueError(
                "Mongo publisher create requires an integer 'id' field for backend switching."
            )

        res = self.col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return self._doc(doc)

    def update(self, publisher_id: int, publisher_data: dict):
        res = self.col.update_one(
            {"id": int(publisher_id)}, {"$set": dict(publisher_data)}
        )
        if res.matched_count == 0:
            return None
        return self.get(publisher_id)

    def delete(self, publisher_id: int) -> bool:
        res = self.col.delete_one({"id": int(publisher_id)})
        return res.deleted_count == 1
