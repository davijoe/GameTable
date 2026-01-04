from neo4j import Driver

from app.repository.video.i_video_repository import IVideoRepository


class VideoRepositoryNeo(IVideoRepository):
    def __init__(self, driver: Driver):
        self.driver = driver

    def _node_to_video(self, node):
        if not node:
            return None
        data = dict(node)
        data["id"] = data.get("id") or 0
        return data

    def get(self, video_id: int):
        with self.driver.session() as session:
            record = session.run(
                "MATCH (v:Video {id: $id}) RETURN v",
                id=int(video_id),
            ).single()
            return self._node_to_video(record["v"]) if record else None

    def list(
        self,
        offset: int,
        limit: int,
        search: str | None,
        sort_by: str | None,
        sort_order: str | None = "asc",
    ):
        with self.driver.session() as session:
            base = "MATCH (v:Video)"
            where = ""
            params = {"skip": offset, "limit": limit}

            if search:
                where = " WHERE v.title CONTAINS $search"
                params["search"] = search

            # for safety
            sort_field = "title"
            sort_dir = "ASC" if (sort_order or "asc") == "asc" else "DESC"

            query = (
                base
                + where
                + f" RETURN v ORDER BY v.{sort_field} {sort_dir} SKIP $skip LIMIT $limit"
            )
            records = session.run(query, **params)
            items = [self._node_to_video(r["v"]) for r in records]

            count_query = base + where + " RETURN count(v) AS count"
            if search:
                count_query = "MATCH (v:Video) WHERE v.title CONTAINS $search RETURN count(v) AS count"
            count_res = session.run(
                count_query, **({"search": search} if search else {})
            ).single()
            total = count_res["count"] if count_res else 0

            return items, total

    def create(self, video_data: dict):
        with self.driver.session() as session:
            session.run(
                """
                CREATE (v:Video $props)
                """,
                props=dict(video_data),
            )
        return dict(video_data)

    def update(self, video_id: int, video_data: dict):
        with self.driver.session() as session:
            record = session.run(
                """
                MATCH (v:Video {id: $id})
                SET v += $props
                RETURN v
                """,
                id=int(video_id),
                props=dict(video_data),
            ).single()
            return self._node_to_video(record["v"]) if record else None

    def delete(self, video_id: int) -> bool:
        with self.driver.session() as session:
            res = session.run(
                """
                MATCH (v:Video {id: $id})
                DETACH DELETE v
                RETURN 1 AS ok
                """,
                id=int(video_id),
            ).single()
            return res is not None
