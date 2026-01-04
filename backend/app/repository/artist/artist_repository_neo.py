from neo4j import Driver

from app.repository.artist.i_artist_repository import IArtistRepository
from app.schema.artist_schema import ArtistCreate, ArtistRead, ArtistUpdate


class ArtistRepositoryNeo(IArtistRepository):
    def __init__(self, driver: Driver):
        self.driver = driver

    def _doc_to_artist(self, node) -> ArtistRead | None:
        if not node:
            return None
        # Only include actual properties
        data = {k: v for k, v in dict(node).items() if not k.startswith("_")}
        data["id"] = data.get("id") or 0
        return ArtistRead(**data)

    def create(self, artist_data) -> ArtistRead:
        # Convert SQLAlchemy/other objects to dict if necessary
        #if hasattr(artist_data, "__dict__"):
        #    data = {k: v for k, v in artist_data.__dict__.items() if v is not None}
        #else:
        #    data = artist_data  # assume dict already

        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                node = self._create_node(tx, artist_data)
                tx.commit()

        return self._doc_to_artist(node)

    def get(self, artist_id: int) -> ArtistRead | None:
        with self.driver.session() as session:
            record = session.run(
                "MATCH (a:Artist) WHERE a.id = $id RETURN a",
                id=int(artist_id),
            ).single()

            if record:
                return self._doc_to_artist(record["a"])
            return None

    def get_by_name(self, name: str) -> ArtistRead | None:
        with self.driver.session() as session:
            record = session.run(
                "MATCH (a:Artist {name: $name}) RETURN a",
                name=name,
            ).single()

            if record:
                return self._doc_to_artist(record["a"])
            return None

    def list(
        self,
        offset: int,
        limit: int,
        search: str | None = None,
    ) -> tuple[list[ArtistRead], int]:
        with self.driver.session() as session:
            query = "MATCH (a:Artist)"
            params = {"skip": offset, "limit": limit}

            if search:
                query += " WHERE a.name CONTAINS $search"
                params["search"] = search

            query += " RETURN a ORDER BY a.name SKIP $skip LIMIT $limit"

            records = session.run(query, **params)
            artists = [self._doc_to_artist(r["a"]) for r in records]

            # Count with optional search
            count_query = "MATCH (a:Artist)"
            count_params = {}
            if search:
                count_query += " WHERE a.name CONTAINS $search"
                count_params["search"] = search
            count_query += " RETURN count(a) AS count"
            count_res = session.run(count_query, **count_params).single()

            total = count_res["count"] if count_res else 0
            return artists, total

    def update(self, artist_id: int, artist_data: ArtistUpdate) -> ArtistRead | None:
        # Convert SQLAlchemy or other objects to dict
        if hasattr(artist_data, "__dict__"):
            update_fields = {k: v for k, v in artist_data.__dict__.items() if v is not None}
        else:
            update_fields = artist_data  # assume dict

        if not update_fields:
            return self.get(artist_id)

        set_clause = ", ".join(f"a.{k} = ${k}" for k in update_fields)
        params = {"id": artist_id, **update_fields}

        with self.driver.session() as session:
            record = session.run(
                f"""
                MATCH (a:Artist {{id: $id}})
                SET {set_clause}
                RETURN a
                """,
                **params,
            ).single()

            if record:
                return self._doc_to_artist(record["a"])
            return None

    def delete(self, artist_id: int) -> bool:
        with self.driver.session() as session:
            res = session.run(
                "MATCH (a:Artist {id: $id}) DETACH DELETE a RETURN COUNT(a) AS deleted",
                id=artist_id,
            ).single()

            return res["deleted"] > 0 if res else False

    @staticmethod
    def _create_node(tx, artist_data: dict):
        query = """
        CREATE (a:Artist {
            id: $id,
            name: $name
        })
        RETURN a
        """
        result = tx.run(query, **artist_data)
        return result.single()["a"]