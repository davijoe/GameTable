from neo4j import Driver

from app.repository.review.i_review_repository import IReviewRepository


class ReviewRepositoryNeo(IReviewRepository):
    def __init__(self, driver: Driver):
        self.driver = driver

    def _node(self, node):
        if not node:
            return None
        data = dict(node)
        data["id"] = int(data.get("id") or 0)
        return data

    def _record_to_review(self, r_node, game_id, u_node):
        if not r_node:
            return None

        r = dict(r_node)
        r["id"] = int(r.get("id") or 0)

        # Required by ReviewRead schema
        r["game_id"] = int(game_id) if game_id is not None else None
        u = dict(u_node) if u_node else None
        if not u:
            return None

        r["user"] = {
            "id": int(u["id"]),
            "display_name": u.get("display_name") or u.get("username") or "Unknown",
        }

        return r

    def get(self, review_id: int):
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (u:User)-[:WROTE]->(r:Review {id: $id})
                MATCH (r)-[:FOR_GAME]-(g:Game)
                RETURN r, g.id AS game_id, u AS user
                """,
                id=int(review_id),
            ).single()

            if not rec:
                return None

            r = dict(rec["r"])
            r["id"] = int(r.get("id") or 0)
            r["game_id"] = int(rec["game_id"])

            u = dict(rec["user"])
            r["user"] = {
                "id": int(u["id"]),
                "display_name": u.get("display_name") or u.get("username"),
            }
            r["user_id"] = int(u["id"])

            return r

    def get_review_count_for_game(self, game_id: int) -> int:
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (:Review)-[:FOR_GAME]-(:Game {id: $game_id})
                RETURN count(*) AS count
                """,
                game_id=int(game_id),
            ).single()

            return rec["count"] if rec else 0

    def list_by_game(self, game_id: int, offset: int, limit: int):
        with self.driver.session() as session:
            recs = session.run(
                """
                MATCH (u:User)-[:WROTE]->(r:Review)-[:FOR_GAME]-(g:Game {id: $game_id})
                RETURN r, g.id AS game_id, u AS user
                ORDER BY r.id DESC
                SKIP $skip LIMIT $limit
                """,
                game_id=int(game_id),
                skip=offset,
                limit=limit,
            )

            items = []
            for rec in recs:
                r = dict(rec["r"])
                r["id"] = int(r.get("id") or 0)
                r["game_id"] = int(rec["game_id"])

                u = dict(rec["user"])
                r["user"] = {
                    "id": int(u["id"]),
                    "display_name": u.get("display_name") or u.get("username"),
                }
                r["user_id"] = int(u["id"])
                items.append(r)

            count_rec = session.run(
                """
                MATCH (:Review)-[:FOR_GAME]-(:Game {id: $game_id})
                RETURN count(*) AS count
                """,
                game_id=int(game_id),
            ).single()
            total = count_rec["count"] if count_rec else 0

            return items, total

    def list(self, offset: int, limit: int, search: str | None):
        with self.driver.session() as session:
            params = {"skip": offset, "limit": limit}
            where = ""
            if search:
                where = " WHERE r.title CONTAINS $search OR r.text CONTAINS $search"
                params["search"] = search

            recs = session.run(
                f"""
                MATCH (u:User)-[:WROTE]->(r:Review)-[:FOR_GAME]-(g:Game)
                {where}
                RETURN r, g.id AS game_id, u AS user
                ORDER BY r.id DESC
                SKIP $skip LIMIT $limit
                """,
                **params,
            )

            items = []
            for rec in recs:
                r = dict(rec["r"])
                r["id"] = int(r.get("id") or 0)
                r["game_id"] = int(rec["game_id"])

                u = dict(rec["user"])
                r["user"] = {
                    "id": int(u["id"]),
                    "display_name": u.get("display_name") or u.get("username"),
                }
                r["user_id"] = int(u["id"])
                items.append(r)

            count_q = f"""
            MATCH (u:User)-[:WROTE]->(r:Review)-[:FOR_GAME]-(g:Game)
            {where}
            RETURN count(r) AS count
            """
            count_rec = session.run(
                count_q, **({"search": search} if search else {})
            ).single()
            total = count_rec["count"] if count_rec else 0

            return items, total

    def create(self, review_data: dict):
        with self.driver.session() as session:
            session.run(
                """
                MATCH (g:Game {id: $game_id})
                MATCH (u:User {id: $user_id})
                CREATE (r:Review $props)
                CREATE (r)-[:FOR_GAME]->(g)
                CREATE (u)-[:WROTE]->(r)
                """,
                game_id=int(review_data["game_id"]),
                user_id=int(review_data["user_id"]),
                props=dict(review_data),
            )
        return dict(review_data)

    def update(self, review_id: int, review_data: dict):
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (r:Review {id: $id})
                SET r += $props
                RETURN r
                """,
                id=int(review_id),
                props=dict(review_data),
            ).single()
            return self._node(rec["r"]) if rec else None

    def delete(self, review_id: int) -> bool:
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (r:Review {id: $id})
                DETACH DELETE r
                RETURN 1 AS ok
                """,
                id=int(review_id),
            ).single()
            return rec is not None
