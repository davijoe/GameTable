import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "source_db")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "rootpassword")

    MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
    MONGODB_PORT = int(os.getenv("MONGODB_PORT", 27017))
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "target_db")
    MONGODB_USER = os.getenv("MONGODB_USER", "admin")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD", "adminpassword")

    NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 1000))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()

