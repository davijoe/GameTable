from datetime import datetime
from src.connectors.mysql_connector import MySQLConnector
from src.connectors.neo4j_connector import Neo4jConnector
from src.transformers.neo4j_transformer import Neo4jTransformer
from src.utils.logger import get_logger

logger = get_logger(__name__)


class MySQLToNeo4jMigration:
    def __init__(self):
        self.mysql_conn = None
        self.neo4j_conn = None
        self._setup_connections()

    def _setup_connections(self):
        try:
            self.mysql_conn = MySQLConnector()
            self.neo4j_conn = Neo4jConnector()
        except Exception as e:
            logger.error(f"Failed to setup connections: {e}")
            self.close_connections()
            raise

    def clear_existing_data(self):
        """Clear ALL existing data in Neo4j including constraints"""
        logger.info("Clearing existing Neo4j data and constraints...")

        try:
            constraints_query = "SHOW CONSTRAINTS"
            constraints = self.neo4j_conn.execute_query(constraints_query)

            for constraint in constraints:
                constraint_name = constraint["name"]
                drop_query = f"DROP CONSTRAINT {constraint_name} IF EXISTS"
                self.neo4j_conn.execute_query(drop_query)
                logger.info(f"Dropped constraint: {constraint_name}")

            indexes_query = "SHOW INDEXES"
            indexes = self.neo4j_conn.execute_query(indexes_query)

            for index in indexes:
                if index.get("name"):
                    index_name = index["name"]
                    drop_query = f"DROP INDEX {index_name} IF EXISTS"
                    self.neo4j_conn.execute_query(drop_query)
                    logger.info(f"Dropped index: {index_name}")

            delete_query = """
            MATCH (n)
            CALL {
                WITH n
                DETACH DELETE n
            } IN TRANSACTIONS OF 10000 ROWS
            """
            self.neo4j_conn.execute_query(delete_query)

            logger.info("Neo4j database completely cleared")

        except Exception as e:
            logger.error(f"Error clearing Neo4j data: {e}")
            raise

    def create_constraints(self):
        """Create constraints for better performance and data integrity"""
        logger.info("Creating Neo4j constraints...")

        constraints = [
            "CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
            "CREATE CONSTRAINT game_id IF NOT EXISTS FOR (g:Game) REQUIRE g.id IS UNIQUE",
            "CREATE CONSTRAINT designer_id IF NOT EXISTS FOR (d:Designer) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT artist_id IF NOT EXISTS FOR (a:Artist) REQUIRE a.id IS UNIQUE",
            "CREATE CONSTRAINT genre_id IF NOT EXISTS FOR (gen:Genre) REQUIRE gen.id IS UNIQUE",
            "CREATE CONSTRAINT publisher_id IF NOT EXISTS FOR (p:Publisher) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT mechanic_id IF NOT EXISTS FOR (m:Mechanic) REQUIRE m.id IS UNIQUE",
            "CREATE CONSTRAINT review_id IF NOT EXISTS FOR (r:Review) REQUIRE r.id IS UNIQUE",
        ]

        for constraint in constraints:
            try:
                self.neo4j_conn.execute_query(constraint)
                logger.info(f"Created constraint: {constraint}")
            except Exception as e:
                logger.warning(
                    f"Could not create constraint {constraint}: {e}",
                )

    def migrate_users(self):
        """Migrate users to Neo4j"""
        logger.info("Starting users migration to Neo4j...")
        try:
            users = self.mysql_conn.get_complete_user_data()
            logger.info(f"Found {len(users)} users to migrate")

            queries = Neo4jTransformer.create_user_nodes(users)

            for i, query_data in enumerate(queries):
                self.neo4j_conn.execute_query(
                    query_data["query"],
                    query_data["params"],
                )
                if (i + 1) % 100 == 0:
                    logger.info(f"Migrated {i + 1}/{len(users)} users")

            logger.info(f"Completed users migration: {len(users)} users")

        except Exception as e:
            logger.error(f"Error in users migration: {e}")
            raise

    def migrate_games_and_related(self):
        """Migrate games, designers, artists, genres, publishers, mechanics and their relationships"""
        logger.info("Starting games and related entities migration...")

        try:
            games = self.mysql_conn.get_complete_game_data()
            designers = self.mysql_conn.get_all_designers()
            artists = self.mysql_conn.get_all_artists()
            genres = self.mysql_conn.get_all_genres()
            publishers = self.mysql_conn.get_all_publishers()
            mechanics = self.mysql_conn.get_all_mechanics()
            videos = self.mysql_conn.get_all_videos()

            logger.info(
                f"Found {len(games)} games, {len(designers)} designers, {
                    len(artists)
                } artists, {len(genres)} genres, {len(publishers)} publishers, {
                    len(mechanics)
                } mechanics, {len(videos)} videos"
            )

            logger.info("Creating Game nodes...")
            game_queries = Neo4jTransformer.create_game_nodes(games)
            self._execute_queries(game_queries, "Game nodes")

            logger.info("Creating Designer nodes...")
            designer_queries = Neo4jTransformer.create_designer_nodes(designers)
            self._execute_queries(designer_queries, "Designer nodes")

            logger.info("Creating Artist nodes...")
            artist_queries = Neo4jTransformer.create_artist_nodes(artists)
            self._execute_queries(artist_queries, "Artist nodes")

            logger.info("Creating Genre nodes...")
            genre_queries = Neo4jTransformer.create_genre_nodes(genres)
            self._execute_queries(genre_queries, "Genre nodes")

            logger.info("Creating Publisher nodes...")
            publisher_queries = Neo4jTransformer.create_publisher_nodes(publishers)
            self._execute_queries(publisher_queries, "Publisher nodes")

            logger.info("Creating Mechanic nodes...")
            mechanic_queries = Neo4jTransformer.create_mechanic_nodes(mechanics)
            self._execute_queries(mechanic_queries, "Mechanic nodes")

            game_designers = self.mysql_conn.get_all_game_designers()
            game_artists = self.mysql_conn.get_all_game_artists()
            game_genres = self.mysql_conn.get_all_game_genres()
            game_publishers = self.mysql_conn.get_all_game_publishers()
            game_mechanics = self.mysql_conn.get_all_game_mechanics()

            logger.info("Creating relationships...")
            relationship_queries = Neo4jTransformer.create_game_relationships(
                game_designers,
                game_artists,
                game_genres,
                game_publishers,
                game_mechanics,
            )
            self._execute_queries(relationship_queries, "relationships")

            logger.info("Completed games and related entities migration")

        except Exception as e:
            logger.error(f"Error in games migration: {e}")
            raise

    def _execute_queries(self, queries, description):
        """Execute a list of queries"""
        if not queries:
            return

        for i, query_data in enumerate(queries):
            try:
                if isinstance(query_data, dict) and "query" in query_data:
                    params = query_data.get("params", {})
                    self.neo4j_conn.execute_query(query_data["query"], params)
                else:
                    logger.warning(
                        f"Invalid query data at index {i} for {description}",
                    )
            except Exception as e:
                logger.warning(
                    f"Error executing query {i} for {description}: {e}",
                )

            if (i + 1) % 100 == 0:
                logger.info(f"Processed {i + 1}/{len(queries)} {description}")

    def migrate_reviews(self):
        """Migrate reviews and their relationships"""
        logger.info("Starting reviews migration...")

        try:
            reviews = self.mysql_conn.get_reviews_with_user_info()

            logger.info(f"Found {len(reviews)} reviews to migrate")

            review_queries = Neo4jTransformer.create_review_nodes_and_relationships(
                reviews
            )

            for i, query_data in enumerate(review_queries):
                self.neo4j_conn.execute_query(
                    query_data["query"],
                    query_data["params"],
                )
                if (i + 1) % 50 == 0:
                    logger.info(
                        f"Created {i + 1}/{
                            len(review_queries)
                        } reviews and relationships"
                    )

            logger.info("Completed reviews migration")

        except Exception as e:
            logger.error(f"Error in reviews migration: {e}")
            raise

    def migrate_all(self):
        """Run complete Neo4j migration"""
        logger.info("Starting complete MySQL to Neo4j migration")
        start_time = datetime.now()

        try:
            self.clear_existing_data()
            self.create_constraints()

            self.migrate_users()
            self.migrate_games_and_related()
            self.migrate_reviews()

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.info(
                f"Neo4j migration completed successfully in {duration:.2f} seconds"
            )

            self._print_statistics()

        except Exception as e:
            logger.error(f"Neo4j migration failed: {e}")
            raise
        finally:
            self.close_connections()

    def _print_statistics(self):
        """Print migration statistics"""
        try:
            stats_queries = {
                "Users": "MATCH (u:User) RETURN count(u) as count",
                "Games": "MATCH (g:Game) RETURN count(g) as count",
                "Designers": "MATCH (d:Designer) RETURN count(d) as count",
                "Artists": "MATCH (a:Artist) RETURN count(a) as count",
                "Genres": "MATCH (gen:Genre) RETURN count(gen) as count",
                "Publishers": "MATCH (p:Publisher) RETURN count(p) as count",
                "Mechanics": "MATCH (m:Mechanic) RETURN count(m) as count",
                "Reviews": "MATCH (r:Review) RETURN count(r) as count",
                "Designer Relationships": "MATCH (g:Game)-[:DESIGNED_BY]->(d:Designer) RETURN count(*) as count",
                "Artist Relationships": "MATCH (g:Game)-[:ART_BY]->(a:Artist) RETURN count(*) as count",
                "Genre Relationships": "MATCH (g:Game)-[:IN_GENRE]->(gen:Genre) RETURN count(*) as count",
                "Publisher Relationships": "MATCH (g:Game)-[:PUBLISHED_BY]->(p:Publisher) RETURN count(*) as count",
                "Mechanic Relationships": "MATCH (g:Game)-[:USES_MECHANIC]->(m:Mechanic) RETURN count(*) as count",
                "Review Relationships": "MATCH (u:User)-[:WROTE]->(r:Review)-[:FOR_GAME]->(g:Game) RETURN count(*) as count",
            }

            logger.info("=== NEO4J MIGRATION STATISTICS ===")
            for label, query in stats_queries.items():
                result = self.neo4j_conn.execute_query(query)
                if result:
                    count = result[0]["count"]
                    logger.info(f"  {label}: {count}")

        except Exception as e:
            logger.warning(f"Could not generate statistics: {e}")

    def close_connections(self):
        if self.mysql_conn:
            self.mysql_conn.close()
        if self.neo4j_conn:
            self.neo4j_conn.close()

