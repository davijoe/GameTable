from datetime import datetime
from src.connectors.mysql_connector import MySQLConnector
from src.connectors.neo4j_connector import Neo4jConnector
from src.transformers.neo4j_transformer import Neo4jTransformer
from src.config.settings import settings
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
        """Clear existing data in Neo4j (optional)"""
        logger.info("Clearing existing Neo4j data...")
        try:
            query = "MATCH (n) DETACH DELETE n"
            self.neo4j_conn.execute_query(query)
            logger.info("Existing Neo4j data cleared")
        except Exception as e:
            logger.warning(f"Could not clear existing data: {e}")
    
    def create_constraints(self):
        """Create constraints for better performance and data integrity"""
        logger.info("Creating Neo4j constraints...")
        
        constraints = [
            "CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
            "CREATE CONSTRAINT game_id IF NOT EXISTS FOR (g:Game) REQUIRE g.id IS UNIQUE",
            "CREATE CONSTRAINT designer_id IF NOT EXISTS FOR (d:Designer) REQUIRE d.id IS UNIQUE",
            "CREATE CONSTRAINT artist_id IF NOT EXISTS FOR (a:Artist) REQUIRE a.id IS UNIQUE",
            "CREATE CONSTRAINT genre_id IF NOT EXISTS FOR (gen:Genre) REQUIRE gen.id IS UNIQUE",
            "CREATE CONSTRAINT review_id IF NOT EXISTS FOR (r:Review) REQUIRE r.id IS UNIQUE",
            "CREATE CONSTRAINT matchup_id IF NOT EXISTS FOR (m:Matchup) REQUIRE m.id IS UNIQUE",
            "CREATE CONSTRAINT move_id IF NOT EXISTS FOR (mv:Move) REQUIRE mv.id IS UNIQUE"
        ]
        
        for constraint in constraints:
            try:
                self.neo4j_conn.execute_query(constraint)
                logger.info(f"Created constraint: {constraint}")
            except Exception as e:
                logger.warning(f"Could not create constraint {constraint}: {e}")
    
    def migrate_users(self):
        """Migrate users to Neo4j"""
        logger.info("Starting users migration to Neo4j...")
        try:
            users = self.mysql_conn.get_complete_user_data()
            logger.info(f"Found {len(users)} users to migrate")
            
            queries = Neo4jTransformer.create_user_nodes(users)
            
            for i, query_data in enumerate(queries):
                self.neo4j_conn.execute_query(query_data['query'], query_data['params'])
                if (i + 1) % 100 == 0:
                    logger.info(f"Migrated {i + 1}/{len(users)} users")
            
            logger.info(f"Completed users migration: {len(users)} users")
            
        except Exception as e:
            logger.error(f"Error in users migration: {e}")
            raise
    
    def migrate_games_and_related(self):
        """Migrate games, designers, artists, genres and their relationships"""
        logger.info("Starting games and related entities migration...")
        
        try:
            games = self.mysql_conn.get_complete_game_data()
            designers = self.mysql_conn.get_all_designers()
            artists = self.mysql_conn.get_all_artists()
            genres = self.mysql_conn.get_all_genres()
            
            logger.info(f"Found {len(games)} games, {len(designers)} designers, {len(artists)} artists, {len(genres)} genres")
            
            game_queries = Neo4jTransformer.create_game_nodes(games)
            designer_artist_queries = Neo4jTransformer.create_designer_artist_nodes(designers, artists)
            genre_queries = Neo4jTransformer.create_genre_nodes(genres)
            
            all_queries = game_queries + designer_artist_queries + genre_queries
            
            for i, query_data in enumerate(all_queries):
                self.neo4j_conn.execute_query(query_data['query'], query_data['params'])
                if (i + 1) % 50 == 0:
                    logger.info(f"Created {i + 1}/{len(all_queries)} game-related nodes")
            
            game_designers = self.mysql_conn.get_all_game_designers()
            game_artists = self.mysql_conn.get_all_game_artists()
            game_genres = self.mysql_conn.get_all_game_genres()
            
            relationship_queries = Neo4jTransformer.create_game_relationships(
                game_designers, game_artists, game_genres
            )
            
            for i, query_data in enumerate(relationship_queries):
                self.neo4j_conn.execute_query(query_data['query'], query_data['params'])
                if (i + 1) % 100 == 0:
                    logger.info(f"Created {i + 1}/{len(relationship_queries)} game relationships")
            
            logger.info("Completed games and related entities migration")
            
        except Exception as e:
            logger.error(f"Error in games migration: {e}")
            raise
    
    def migrate_social_relationships(self):
        """Migrate friendships and messages"""
        logger.info("Starting social relationships migration...")
        
        try:
            friendships = self.mysql_conn.get_all_friendships()
            friendship_queries = Neo4jTransformer.create_friendship_relationships(friendships)
            
            for i, query_data in enumerate(friendship_queries):
                self.neo4j_conn.execute_query(query_data['query'], query_data['params'])
                if (i + 1) % 50 == 0:
                    logger.info(f"Created {i + 1}/{len(friendship_queries)} friendships")
            
            messages = self.mysql_conn.get_all_messages()
            message_queries = Neo4jTransformer.create_message_relationships(messages)
            
            for i, query_data in enumerate(message_queries):
                self.neo4j_conn.execute_query(query_data['query'], query_data['params'])
                if (i + 1) % 100 == 0:
                    logger.info(f"Created {i + 1}/{len(message_queries)} messages")
            
            logger.info(f"Completed social relationships: {len(friendship_queries)} friendships, {len(message_queries)} messages")
            
        except Exception as e:
            logger.error(f"Error in social relationships migration: {e}")
            raise
    
    def migrate_reviews(self):
        """Migrate reviews and their relationships"""
        logger.info("Starting reviews migration...")
        
        try:
            reviews = self.mysql_conn.get_all_reviews()
            game_reviews = self.mysql_conn.get_all_game_reviews()
            
            logger.info(f"Found {len(reviews)} reviews and {len(game_reviews)} game-review relationships")
            
            review_queries = Neo4jTransformer.create_review_nodes_and_relationships(reviews, [], [])
            
            for i, query_data in enumerate(review_queries):
                self.neo4j_conn.execute_query(query_data['query'], query_data['params'])
                if (i + 1) % 50 == 0:
                    logger.info(f"Created {i + 1}/{len(review_queries)} reviews")
            
            game_review_queries = Neo4jTransformer.create_game_review_relationships(game_reviews)
            
            for i, query_data in enumerate(game_review_queries):
                self.neo4j_conn.execute_query(query_data['query'], query_data['params'])
                if (i + 1) % 50 == 0:
                    logger.info(f"Created {i + 1}/{len(game_review_queries)} game-review relationships")
            
            logger.info("Completed reviews migration")
            
        except Exception as e:
            logger.error(f"Error in reviews migration: {e}")
            raise
    
    def migrate_matchups(self):
        """Migrate matchups and their relationships"""
        logger.info("Starting matchups migration...")
        
        try:
            matchups = self.mysql_conn.get_complete_matchup_data()
            users = self.mysql_conn.get_complete_user_data()
            games = self.mysql_conn.get_complete_game_data()
            
            logger.info(f"Found {len(matchups)} matchups to migrate")
            
            matchup_queries = Neo4jTransformer.create_matchup_nodes_and_relationships(
                matchups, users, games
            )
            
            for i, query_data in enumerate(matchup_queries):
                self.neo4j_conn.execute_query(query_data['query'], query_data['params'])
                if (i + 1) % 20 == 0:
                    logger.info(f"Processed {i + 1}/{len(matchup_queries)} matchup queries")
            
            logger.info("Completed matchups migration")
            
        except Exception as e:
            logger.error(f"Error in matchups migration: {e}")
            raise
    
    def migrate_spectators(self):
        """Migrate spectator relationships"""
        logger.info("Starting spectators migration...")
        
        try:
            spectators = self.mysql_conn.get_all_spectators_with_users()
            logger.info(f"Found {len(spectators)} spectator relationships")
            
            spectator_queries = Neo4jTransformer.create_spectator_relationships(spectators)
            
            for i, query_data in enumerate(spectator_queries):
                self.neo4j_conn.execute_query(query_data['query'], query_data['params'])
                if (i + 1) % 50 == 0:
                    logger.info(f"Created {i + 1}/{len(spectator_queries)} spectator relationships")
            
            logger.info("Completed spectators migration")
            
        except Exception as e:
            logger.error(f"Error in spectators migration: {e}")
            raise
    
    def migrate_moves(self):
        """Migrate moves and their relationships"""
        logger.info("Starting moves migration...")
        
        try:
            moves = self.mysql_conn.get_all_moves()
            matchup_moves = self.mysql_conn.get_all_matchup_moves()
            
            logger.info(f"Found {len(moves)} moves and {len(matchup_moves)} matchup-move relationships")
            
            move_queries = Neo4jTransformer.create_move_nodes_and_relationships(moves, matchup_moves)
            
            for i, query_data in enumerate(move_queries):
                self.neo4j_conn.execute_query(query_data['query'], query_data['params'])
                if (i + 1) % 100 == 0:
                    logger.info(f"Processed {i + 1}/{len(move_queries)} move queries")
            
            logger.info("Completed moves migration")
            
        except Exception as e:
            logger.error(f"Error in moves migration: {e}")
            raise
    
    def migrate_all(self):
        """Run complete Neo4j migration"""
        logger.info("Starting complete MySQL to Neo4j migration")
        start_time = datetime.now()
        
        try:
            self.create_constraints()
            
            self.migrate_users()
            self.migrate_games_and_related()
            self.migrate_social_relationships()
            self.migrate_reviews()
            self.migrate_matchups()
            self.migrate_spectators()
            self.migrate_moves()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            logger.info(f"Neo4j migration completed successfully in {duration:.2f} seconds")
            
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
                "Reviews": "MATCH (r:Review) RETURN count(r) as count",
                "Matchups": "MATCH (m:Matchup) RETURN count(m) as count",
                "Moves": "MATCH (mv:Move) RETURN count(mv) as count",
                "Friendships": "MATCH ()-[f:FRIENDS_WITH]->() RETURN count(f) as count",
                "Messages": "MATCH ()-[m:MESSAGED]->() RETURN count(m) as count"
            }
            
            logger.info("=== NEO4J MIGRATION STATISTICS ===")
            for label, query in stats_queries.items():
                result = self.neo4j_conn.execute_query(query)
                if result:
                    count = result[0]['count']
                    logger.info(f"  {label}: {count}")
            
        except Exception as e:
            logger.warning(f"Could not generate statistics: {e}")
    
    def close_connections(self):
        if self.mysql_conn:
            self.mysql_conn.close()
        if self.neo4j_conn:
            self.neo4j_conn.close()