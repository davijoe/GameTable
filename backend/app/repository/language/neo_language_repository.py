from neo4j import Driver

from app.repository.language.i_language_repository import ILanguageRepository


class LanguageRepositoryNeo(ILanguageRepository):
    def __init__(self, driver: Driver):
        self.driver = driver

    def _node(self, node):
        if not node:
            return None
        d = dict(node)
        if "id" in d:
            d["id"] = int(d["id"])
        return d

    def get(self, language_id: int):
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (l:Language {id: $id})
                RETURN l
                """,
                id=int(language_id),
            ).single()
            return self._node(rec["l"]) if rec else None

    def get_by_name(self, name: str):
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (l:Language {language: $name})
                RETURN l
                """,
                name=name,
            ).single()
            return self._node(rec["l"]) if rec else None

    def list(self, offset: int, limit: int, search: str | None):
        with self.driver.session() as session:
            params = {"skip": int(offset), "limit": int(limit)}
            where = ""
            if search:
                where = "WHERE l.language CONTAINS $search"
                params["search"] = search

            recs = session.run(
                f"""
                MATCH (l:Language)
                {where}
                RETURN l
                ORDER BY l.id DESC
                SKIP $skip LIMIT $limit
                """,
                **params,
            )

            items = [self._node(r["l"]) for r in recs]

            count_rec = session.run(
                f"""
                MATCH (l:Language)
                {where}
                RETURN count(l) AS count
                """,
                **({"search": search} if search else {}),
            ).single()

            total = int(count_rec["count"]) if count_rec else 0
            return items, total

    def create(self, language_data):
        with self.driver.session() as session:
            session.run(
                """
                CREATE (l:Language $props)
                """,
                props=dict(language_data),
            )
        return dict(language_data)

    def update(self, language_id: int, language_data):
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (l:Language {id: $id})
                SET l += $props
                RETURN l
                """,
                id=int(language_id),
                props=dict(language_data),
            ).single()
            return self._node(rec["l"]) if rec else None

    def delete(self, language_id: int) -> bool:
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (l:Language {id: $id})
                DETACH DELETE l
                RETURN 1 AS ok
                """,
                id=int(language_id),
            ).single()
            return rec is not None
