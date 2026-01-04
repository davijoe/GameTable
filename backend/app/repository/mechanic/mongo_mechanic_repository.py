from pymongo.collection import Collection

from app.repository.mechanic.i_mechanic_repository import IMechanicRepository


class MechanicRepositoryMongo(IMechanicRepository):
    def __init__(self, db):
        self.games: Collection = db["games"]

    def get(self, mechanic_id: int):
        mid = int(mechanic_id)
        pipeline = [
            {"$match": {"mechanics.id": mid}},
            {"$unwind": "$mechanics"},
            {"$match": {"mechanics.id": mid}},
            {"$replaceRoot": {"newRoot": "$mechanics"}},
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
            {"$match": {"mechanics.name": {"$regex": f"^{name}$", "$options": "i"}}},
            {"$unwind": "$mechanics"},
            {"$match": {"mechanics.name": {"$regex": f"^{name}$", "$options": "i"}}},
            {"$replaceRoot": {"newRoot": "$mechanics"}},
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
        sort_by: str | None,
        sort_order: str | None = "asc",
    ):
        sort_dir = 1 if (sort_order or "asc") == "asc" else -1

        pipeline: list[dict] = [
            {"$unwind": "$mechanics"},
        ]

        if search:
            pipeline.append(
                {"$match": {"mechanics.name": {"$regex": search, "$options": "i"}}}
            )

        # group to unique mechanics
        pipeline += [
            {
                "$group": {
                    "_id": "$mechanics.id",
                    "id": {"$first": "$mechanics.id"},
                    "name": {"$first": "$mechanics.name"},
                }
            },
            {"$sort": {"name": sort_dir}},
        ]

        count_docs = list(self.games.aggregate(pipeline + [{"$count": "count"}]))
        total = int(count_docs[0]["count"]) if count_docs else 0

        items = list(
            self.games.aggregate(
                pipeline + [{"$skip": int(offset)}, {"$limit": int(limit)}]
            )
        )
        for it in items:
            it["id"] = int(it["id"])
        return items, total

    def create(self, mechanic_data: dict):
        raise NotImplementedError(
            "Mechanics are embedded in games in Mongo. Create them by updating game documents or normalize into a mechanics collection."
        )

    def update(self, mechanic_id: int, mechanic_data: dict):
        raise NotImplementedError(
            "Mechanics are embedded in games in Mongo. Update embedded mechanics in game documents or normalize into a mechanics collection."
        )

    def delete(self, mechanic_id: int) -> bool:
        raise NotImplementedError(
            "Mechanics are embedded in games in Mongo. Delete embedded mechanics from game documents or normalize into a mechanics collection."
        )
