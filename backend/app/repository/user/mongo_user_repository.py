from pymongo.collection import Collection

from app.repository.user.i_user_repository import IUserRepository


class UserRepositoryMongo(IUserRepository):
    def __init__(self, db):
        self.col: Collection = db["users"]

    def _doc(self, doc: dict | None):
        if not doc:
            return None
        doc["id"] = doc.get("id", doc.get("_id"))
        return doc

    def get(self, user_id: int):
        doc = self.col.find_one({"id": int(user_id)}) or self.col.find_one(
            {"_id": int(user_id)}
        )
        return self._doc(doc)

    def get_by_username(self, username: str):
        return self._doc(self.col.find_one({"username": username}))

    def get_by_email(self, email: str):
        return self._doc(self.col.find_one({"email": email}))

    def list(self, offset: int, limit: int, search: str | None):
        query = {}
        if search:
            query["$or"] = [
                {"username": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
            ]

        total = self.col.count_documents(query)
        cursor = self.col.find(query).skip(offset).limit(limit).sort("username", 1)
        return [self._doc(d) for d in cursor], total

    def create(self, user_data: dict):
        doc = dict(user_data)
        if "id" not in doc and "_id" not in doc:
            raise ValueError(
                "Mongo user create requires integer 'id' for backend switching."
            )
        res = self.col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return self._doc(doc)

    def update(self, user_id: int, user_data: dict):
        res = self.col.update_one({"id": int(user_id)}, {"$set": dict(user_data)})
        if res.matched_count == 0:
            return None
        return self.get(user_id)

    def delete(self, user_id: int) -> bool:
        res = self.col.delete_one({"id": int(user_id)})
        return res.deleted_count == 1
