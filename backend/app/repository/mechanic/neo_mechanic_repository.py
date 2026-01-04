from neo4j import Driver

from app.repository.mechanic.i_mechanic_repository import IMechanicRepository


class MechanicRepositoryNeo(IMechanicRepository):
    def __init__(self, driver: Driver):
        self.driver = driver

    def _node(self, node):
        if not node:
            return None
        data = dict(node)
        data["id"] = int(data.get("id") or 0)
        return data

    def get(self, mechanic_id: int):
        with self.driver.session() as session:
            rec = session.run(
                "MATCH (m:Mechanic {id: $id}) RETURN m",
                id=int(mechanic_id),
            ).single()
            return self._node(rec["m"]) if rec else None

    def get_by_name(self, name: str):
        with self.driver.session() as session:
            rec = session.run(
                "MATCH (m:Mechanic {name: $name}) RETURN m",
                name=name,
            ).single()
            return self._node(rec["m"]) if rec else None

    def list(
        self,
        offset: int,
        limit: int,
        search: str | None,
        sort_by: str | None,
        sort_order: str | None = "asc",
    ):
        with self.driver.session() as session:
            base = "MATCH (m:Mechanic)"
            where = ""
            params = {"skip": int(offset), "limit": int(limit)}

            if search:
                where = " WHERE m.name CONTAINS $search"
                params["search"] = search

            sort_field = "name" if (sort_by in (None, "name")) else "name"
            sort_dir = "ASC" if (sort_order or "asc") == "asc" else "DESC"

            query = (
                base
                + where
                + f" RETURN m ORDER BY m.{sort_field} {sort_dir} SKIP $skip LIMIT $limit"
            )
            records = session.run(query, **params)
            items = [self._node(r["m"]) for r in records]

            count_q = base + where + " RETURN count(m) AS count"
            count_res = session.run(
                count_q, **({"search": search} if search else {})
            ).single()
            total = int(count_res["count"]) if count_res else 0

            return items, total

    def create(self, mechanic_data: dict):
        with self.driver.session() as session:
            session.run(
                """
                CREATE (m:Mechanic {
                    id: $id,
                    name: $name
                })
                """,
                **mechanic_data,
            )
        return dict(mechanic_data)

    def update(self, mechanic_id: int, mechanic_data: dict):
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (m:Mechanic {id: $id})
                SET m += $props
                RETURN m
                """,
                id=int(mechanic_id),
                props=dict(mechanic_data),
            ).single()
            return self._node(rec["m"]) if rec else None

    def delete(self, mechanic_id: int) -> bool:
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (m:Mechanic {id: $id})
                DETACH DELETE m
                RETURN 1 AS ok
                """,
                id=int(mechanic_id),
            ).single()
            return rec is not None
