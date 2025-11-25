import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.migrations.mysql_to_mongodb import MySQLToMongoDBMigration
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    try:
        logger.info("Starting MySQL to MongoDB migration with data nesting")
        start_time = time.time()
        
        migration = MySQLToMongoDBMigration()
        migration.migrate_all()
        
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"Migration completed in {duration:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()