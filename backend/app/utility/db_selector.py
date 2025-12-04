import os

DB_MODE = os.getenv("DB_MODE", "sql").lower()

def select_repo(sql_repo, mongo_repo, neo_repo):
    if DB_MODE == "sql":
        return sql_repo
    elif DB_MODE == "mongo":
        return mongo_repo
    elif DB_MODE == "neo":
        return neo_repo
    else:
        raise ValueError(f"Wrong DB_MODE: {DB_MODE}")