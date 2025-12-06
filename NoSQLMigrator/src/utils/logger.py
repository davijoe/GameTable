import logging
import sys
import os


def setup_logger():
    logger = logging.getLogger("data_migration")

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    try:
        file_handler = logging.FileHandler("migration.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        print(f"Log file created at: {os.path.abspath('migration.log')}")
    except Exception as e:
        print(f"Could not create log file: {e}")

    logger.propagate = False

    return logger


logger = setup_logger()


def get_logger(name):
    """Get logger for specific module"""
    return logging.getLogger(f"data_migration.{name}")

