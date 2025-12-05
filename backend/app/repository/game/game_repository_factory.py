import os
from app.utility.db_sql import get_sql_db
from app.utility.db_mongo import get_db as get_mongo_db
#from app.utility.db_sql_neo import get_neo
from app.repository.game.sql_game_repository import GameRepositorySQL
from app.repository.game.mongo_game_repository import GameRepositoryMongo
#from app.repository.game.neo_game_repository import GameRepositoryNeo


DB_MODE = os.getenv("DB_MODE", "sql").lower()

def get_game_repository():
	if DB_MODE == "sql":
		db = next(get_sql_db())
		return GameRepositorySQL(db)
	elif DB_MODE == "mongo":
		db = next(get_mongo_db())
		return GameRepositoryMongo(db)
	elif DB_MODE == "neo":
		pass
		#return GameRepositoryNeo(get_neo())

	raise ValueError(f"Unknown DB_MODE: {DB_MODE}")
