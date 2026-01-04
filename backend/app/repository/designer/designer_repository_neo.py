from neo4j import Driver

from app.repository.designer.i_designer_repository import IDesignerRepository


class DesignerRepositoryNeo(IDesignerRepository):
    def __init__(self, driver: Driver):
        self.driver = driver

    def _node(self, node):
        if not node:
            return None
        data = dict(node)
        data["id"] = int(data.get("id") or 0)
        return data

    def get(self, designer_id: int):
        with self.driver.session() as session:
            rec = session.run(
                "MATCH (p:Designer {id: $id}) RETURN p",
                id=int(designer_id),
            ).single()
            return self._node(rec["p"]) if rec else None

    def get_by_name(self, name: str):
        with self.driver.session() as session:
            rec = session.run(
                "MATCH (p:Designer {name: $name}) RETURN p",
                name=name,
            ).single()
            return self._node(rec["p"]) if rec else None

    def list(
        self,
        offset: int,
        limit: int,
        search: str | None,
        sort_order: str | None = "asc",
    ):
        with self.driver.session() as session:
            base = "MATCH (p:Designer)"
            where = ""
            params = {"skip": offset, "limit": limit}

            if search:
                where = " WHERE p.name CONTAINS $search"
                params["search"] = search

            sort_field = "name"
            sort_dir = "ASC" if (sort_order or "asc") == "asc" else "DESC"

            query = (
                base
                + where
                + f" RETURN p ORDER BY p.{sort_field} {
                    sort_dir
                } SKIP $skip LIMIT $limit"
            )
            records = session.run(query, **params)
            items = [self._node(r["p"]) for r in records]

            count_q = base + where + " RETURN count(p) AS count"
            count_res = session.run(
                count_q, **({"search": search} if search else {})
            ).single()
            total = count_res["count"] if count_res else 0

            return items, total

    def create(self, designer_data: dict):
        with self.driver.session() as session:
            session.run(
                """
                CREATE (p:Designer {
                    id: $id,
                    name: $name
                })
                """,
                **designer_data,
            )
        return dict(designer_data)

    def update(self, designer_id: int, designer_data: dict):
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (p:Designer {id: $id})
                SET p += $props
                RETURN p
                """,
                id=int(designer_id),
                props=dict(designer_data),
            ).single()
            return self._node(rec["p"]) if rec else None

    def delete(self, designer_id: int) -> bool:
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (p:Designer {id: $id})
                DETACH DELETE p
                RETURN 1 AS ok
                """,
                id=int(designer_id),
            ).single()
            return rec is not None
