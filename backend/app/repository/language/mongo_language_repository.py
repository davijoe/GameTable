from pymongo.collection import Collection

from app.repository.language.i_language_repository import ILanguageRepository


class LanguageRepositoryMongo(ILanguageRepository):
    def __init__(self, db):
        self.col: Collection = db["languages"]

    def _doc(self, doc: dict | None):
        if not doc:
            return None
        doc["id"] = int(doc.get("id", doc.get("_id")))
        return doc

    def get(self, language_id: int):
        lid = int(language_id)
        doc = self.col.find_one({"id": lid})
        return self._doc(doc)

    def get_by_name(self, name: str):
        doc = self.col.find_one({"language": name})
        return self._doc(doc)

    def list(self, offset: int, limit: int, search: str | None):
        query = {}
        if search:
            query["language"] = {"$regex": search, "$options": "i"}

        total = self.col.count_documents(query)
        cursor = self.col.find(query).sort("id", -1).skip(int(offset)).limit(int(limit))
        return [self._doc(d) for d in cursor], total

    def create(self, language_data):
        doc = dict(language_data)

        if "id" not in doc:
            raise ValueError(
                "Mongo language create requires integer 'id' for backend switching."
            )

        self.col.insert_one(doc)
        return self._doc(doc)

    def update(self, language_id: int, language_data):
        lid = int(language_id)
        res = self.col.update_one({"id": lid}, {"$set": dict(language_data)})
        if res.matched_count == 0:
            return None
        return self.get(lid)

    def delete(self, language_id: int) -> bool:
        lid = int(language_id)
        res = self.col.delete_one({"id": lid})
        return res.deleted_count == 1
