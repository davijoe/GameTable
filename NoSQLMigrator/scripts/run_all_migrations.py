from src.utils.logger import get_logger
import sys
import os
import time
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


logger = get_logger(__name__)


def run_migration(script_name):
    """Run a migration script and return success status"""
    logger.info(f"Starting {script_name}...")
    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=3601,
        )

        duration = time.time() - start_time

        if result.returncode == 0:
            logger.info(
                f"{script_name} completed successfully in {duration:.2f}s",
            )
            return True
        else:
            logger.error(f"{script_name} failed after {duration:.2f}s")
            logger.error(f"STDERR: {result.stderr}")
            logger.error(f"STDOUT: {result.stdout}")
            return False

    except subprocess.TimeoutExpired:
        logger.error(f"{script_name} timed out after 1 hour")
        return False
    except Exception as e:
        logger.error(f"{script_name} failed with exception: {e}")
        return False


def main():
    logger.info("Starting all database migrations...")

    mongo_success = run_migration("scripts/run_migration.py")

    if mongo_success:
        neo4j_success = run_migration("scripts/run_neo4j_migration.py")

        if neo4j_success:
            logger.info("All migrations completed successfully")
            return 0
        else:
            logger.error("Neo4j migration failed")
            return 1
    else:
        logger.error("MongoDB migration failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

