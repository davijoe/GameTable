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

    def get(self, review_id: int):
        with self.driver.session() as session:
            rec = session.run(
                "MATCH (r:Review {id: $id}) RETURN r",
                id=int(review_id),
            ).single()
            return self._node(rec["r"]) if rec else None

    def get_review_count_for_game(self, game_id: int) -> int:
        with self.driver.session() as session:
            rec = session.run(
                """
                MATCH (g:Game {id: $game_id})-[:HAS_REVIEW]->(r:Review)
                RETURN count(r) AS count
                """,
                game_id=int(game_id),
            ).single()
            return rec["count"] if rec else 0

    def list_by_game(self, game_id: int, offset: int, limit: int):
        with self.driver.session() as session:
            params = {"game_id": int(game_id), "skip": offset, "limit": limit}

            recs = session.run(
                """
                MATCH (g:Game {id: $game_id})-[:HAS_REVIEW]->(r:Review)
                RETURN r
                ORDER BY r.id DESC
                SKIP $skip LIMIT $limit
                """,
                **params,
            )
            items = [self._node(r["r"]) for r in recs]

            count_rec = session.run(
                """
                MATCH (g:Game {id: $game_id})-[:HAS_REVIEW]->(r:Review)
                RETURN count(r) AS count
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
                where = " WHERE r.comment CONTAINS $search"
                params["search"] = search

            recs = session.run(
                f"""
                MATCH (r:Review)
                {where}
                RETURN r
                ORDER BY r.id DESC
                SKIP $skip LIMIT $limit
                """,
                **params,
            )
            items = [self._node(r["r"]) for r in recs]

            count_q = f"MATCH (r:Review){where} RETURN count(r) AS count"
            count_rec = session.run(
                count_q, **({"search": search} if search else {})
            ).single()
            total = count_rec["count"] if count_rec else 0

            return items, total

    def create(self, review_data: dict):
        # Expect review_data to include at least: id, game_id, plus review fields.
        with self.driver.session() as session:
            session.run(
                """
                MATCH (g:Game {id: $game_id})
                CREATE (r:Review $props)
                CREATE (g)-[:HAS_REVIEW]->(r)
                """,
                game_id=int(review_data["game_id"]),
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
