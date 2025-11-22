from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class Neo4jConnector:
    def __init__(self):
        self.driver = None
        self.connect()
    
    def connect(self):
        try:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )

            self.driver.verify_connectivity()
            logger.info("Connected to Neo4j successfully")
        except ServiceUnavailable as e:
            logger.error(f"Error connecting to Neo4j: {e}")
            raise
    
    def execute_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return list(result)
    
    def create_constraints(self):
        """Create necessary constraints for the graph"""
        constraints = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Product) REQUIRE p.id IS UNIQUE",

        ]
        
        for constraint in constraints:
            try:
                self.execute_query(constraint)
                logger.info(f"Created constraint: {constraint}")
            except Exception as e:
                logger.warning(f"Could not create constraint {constraint}: {e}")
    
    def close(self):
        if self.driver:
            self.driver.close()
            logger.info("Neo4j connection closed")