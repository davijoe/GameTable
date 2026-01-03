from neo4j import Driver

from app.repository.user.i_user_repository import IUserRepository


class UserRepositoryNeo(IUserRepository):
    def __init__(self, driver: Driver):
        self.driver = driver

    def _node(self, node):
        if not node:
            return None
        data = dict(node)
        data["id"] = int(data.get("id") or 0)
        return data

    def get(self, user_id: int):
        with self.driver.session() as session:
            rec = session.run(
                "MATCH (u:User {id: $id}) RETURN u",
                id=int(user_id),
            ).single()
            return self._node(rec["u"]) if rec else None

    def get_by_username(self, username: str):
        with self.driver.session() as session:
            rec = session.run(
                "MATCH (u:User {username: $username}) RETURN u",
                username=username,
            ).single()
            return self._node(rec["u"]) if rec else None

    def get_by_email(self, email: str):
        with self.driver.session() as session:
            rec = session.run(
                "MATCH (u:User {email: $email}) RETURN u",
                email=email,
            ).single()
            return self._node(rec["u"]) if rec else None

    def list(self, offset: int, limit: int, search: str | None):
        with self.driver.session() as session:
            base = "MATCH (u:User)"
            where = ""
            params = {"skip": offset, "limit": limit}

            if search:
                where = " WHERE u.username CONTAINS $search OR u.email CONTAINS $search"
                params["search"] = search

            query = (
                base + where + " RETURN u ORDER BY u.username SKIP $skip LIMIT $limit"
            )
            records = session.run(query, **params)
            items = [self._node(r["u"]) for r in records]

            count_q = base + where + " RETURN count(u) AS count"
            count_rec = session.run(
                count_q, **({"search": search} if search else {})
            ).single()
            total = count_rec["count"] if count_rec else 0

            return items, total

    def create(self, user_data: dict):
        with self.driver.session() as session:
            session.run(
                """
                CREATE (u:User $props)
                """,
                props=dict(user_data),
            )
        return dict(user_data)

    def update(self, user_id: int, user_data: dict):
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (u:User {id: $id})
                SET u += $props
                RETURN u
                """,
                id=int(user_id),
                props=dict(user_data),
            ).single()
            return self._node(rec["u"]) if rec else None

    def delete(self, user_id: int) -> bool:
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (u:User {id: $id})
                DETACH DELETE u
                RETURN 1 AS ok
                """,
                id=int(user_id),
            ).single()
            return rec is not None
