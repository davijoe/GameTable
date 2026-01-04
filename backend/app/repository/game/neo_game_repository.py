from neo4j import Driver

from app.repository.game.i_game_repository import IGameRepository
from app.schema.artist_schema import ArtistRead
from app.schema.designer_schema import DesignerRead
from app.schema.game_schema import GameCreate, GameDetail, GameRead, GameUpdate
from app.schema.mechanic_schema import MechanicRead
from app.schema.publisher_schema import PublisherRead


class GameRepositoryNeo(IGameRepository):
    SORT_FIELDS = {
        "bgg_rating": "g.bgg_rating",
        "year_published": "g.year_published",
        "playing_time": "g.playing_time",
        "name": "g.name",
    }

    def __init__(self, driver: Driver):
        self.driver = driver

    def _doc_to_game(self, record: dict) -> GameRead:
        if not record:
            return None
        data = dict(record)
        data["id"] = data.get("id") or 0
        return GameRead(**data)

    def create(self, game_data: GameCreate) -> GameRead:
        with self.driver.session() as session:
            session.write_transaction(self._create_node, game_data)
        return GameRead(id=game_data.id or 0, **game_data.model_dump())

    def get(self, game_id: int) -> GameRead | None:
        with self.driver.session() as session:
            query = "MATCH (g:Game) WHERE g.id = $game_id RETURN g"
            # casting to int is apparently important
            record = session.run(query, game_id=int(game_id)).single()
            if record:
                return self._doc_to_game(record["g"])
        return None

    def list(
        self,
        offset: int,
        limit: int,
        search: str | None = None,
        sort_by: str | None = None,
        sort_order: str = "desc",
    ) -> tuple[list[GameRead], int]:
        with self.driver.session() as session:
            params = {"skip": offset, "limit": limit}

            query = "MATCH (g:Game)"
            if search:
                query += " WHERE g.name CONTAINS $search"
                params["search"] = search

            if sort_by in self.SORT_FIELDS:
                order = "DESC" if sort_order == "desc" else "ASC"
                query += f" RETURN g ORDER BY {self.SORT_FIELDS[sort_by]} {order} SKIP $skip LIMIT $limit"
            else:
                query += " RETURN g ORDER BY g.name ASC SKIP $skip LIMIT $limit"

            records = session.run(query, **params)
            games = [self._doc_to_game(record["g"]) for record in records]

            count_query = "MATCH (g:Game)"
            if search:
                count_query += " WHERE g.name CONTAINS $search"
            count_query += " RETURN count(g) AS count"
            count_res = session.run(count_query, **({"search": search} if search else {})).single()
            total = count_res["count"] if count_res else 0

            return games, total

    def update(self, game_id: int, game_data: GameUpdate) -> GameRead | None:
        update_fields = game_data.model_dump(exclude_unset=True)
        if not update_fields:
            return self.get(game_id)

        with self.driver.session() as session:
            set_clauses = ", ".join([f"g.{k} = ${k}" for k in update_fields.keys()])
            params = {"id": game_id, **update_fields}
            query = f"MATCH (g:Game {{id: $id}}) SET {set_clauses} RETURN g"
            record = session.run(query, **params).single()
            if record:
                return self._doc_to_game(record["g"])
            return None

    def delete(self, game_id: int) -> bool:
        with self.driver.session() as session:
            res = session.run(
                "MATCH (g:Game {id: $id}) DETACH DELETE g RETURN COUNT(g) AS deleted",
                id=game_id,
            ).single()
            return res["deleted"] > 0 if res else False

    @staticmethod
    def _create_node(tx, game_data: GameCreate):
        query = """
        CREATE (g:Game {
            id: $id,
            name: $name,
            slug: $slug,
            year_published: $year_published,
            bgg_rating: $bgg_rating,
            difficulty_rating: $difficulty_rating,
            description: $description,
            playing_time: $playing_time,
            available: $available,
            min_players: $min_players,
            max_players: $max_players,
            image: $image,
            thumbnail: $thumbnail
        })
        """

        tx.run(query, **game_data.model_dump())

    def get_detail(self, game_id: int) -> GameDetail | None:
        """Return a game with all related nodes (artists, designers, publishers, mechanics)."""
        with self.driver.session() as session:
            query = """
            MATCH (g:Game {id: $id})
            OPTIONAL MATCH (g)-[:ART_BY]->(a:Artist)
            OPTIONAL MATCH (g)-[:DESIGNED_BY]->(d:Designer)
            OPTIONAL MATCH (g)-[:PUBLISHED_BY]->(p:Publisher)
            OPTIONAL MATCH (g)-[:USES_MECHANIC]->(m:Mechanic)
            RETURN g,
                collect(DISTINCT a) AS artists,
                collect(DISTINCT d) AS designers,
                collect(DISTINCT p) AS publishers,
                collect(DISTINCT m) AS mechanics
            """
            record = session.run(query, id=int(game_id)).single()
            if not record:
                return None

            g = self._doc_to_game(record["g"])
            return GameDetail.model_validate(
                {
                    **g.model_dump(),
                    "artists": list(record["artists"]),
                    "designers": list(record["designers"]),
                    "publishers": list(record["publishers"]),
                    "mechanics": list(record["mechanics"]),
                }
            )

    @staticmethod
    def _get_node(tx, game_id: int):
        query = "MATCH (g:Game {id: $id}) RETURN g"
        record = tx.run(query, id=game_id).single()
        if record:
            return record["g"]
        return None
