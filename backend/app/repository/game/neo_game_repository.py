# app/repository/game/neo_game_repository.py
from typing import Optional, List, Tuple
from app.schema.game_schema import GameCreate, GameRead, GameUpdate
from neo4j import Driver
from app.repository.game.i_game_repository import IGameRepository

class GameRepositoryNeo(IGameRepository):
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

	def get(self, game_id: int) -> Optional[GameRead]:
		with self.driver.session() as session:
			query = "MATCH (g:Game) WHERE g.id = $game_id RETURN g"
			record = session.run(query, game_id=int(game_id)).single() # casting to int is apparently important
			if record:
				return self._doc_to_game(record["g"])
		return None
		
	def list(self, offset: int, limit: int, search: Optional[str] = None) -> Tuple[List[GameRead], int]:
		with self.driver.session() as session:
			query = "MATCH (g:Game)"
			params = {"skip": offset, "limit": limit}
			if search:
				query += " WHERE g.name CONTAINS $search"
				params["search"] = search
			query += " RETURN g ORDER BY g.name SKIP $skip LIMIT $limit"
			records = session.run(query, **params)
			games = [self._doc_to_game(record["g"]) for record in records]

			count_res = session.run("MATCH (g:Game) RETURN count(g) AS count").single()
			total = count_res["count"] if count_res else 0

			return games, total

	def update(self, game_id: int, game_data: GameUpdate) -> Optional[GameRead]:
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

	@staticmethod
	def _get_node(tx, game_id: int):
		query = "MATCH (g:Game {id: $id}) RETURN g"
		record = tx.run(query, id=game_id).single()
		if record:
			return record["g"]
		return None
