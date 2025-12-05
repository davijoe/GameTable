import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.migrations.mysql_to_neo4j import MySQLToNeo4jMigration
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    try:
        logger.info("Starting MySQL to Neo4j migration")
        start_time = time.time()
        
        migration = MySQLToNeo4jMigration()
        migration.clear_existing_data()
        migration.migrate_all()
        
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"Neo4j migration completed in {duration:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Neo4j migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()