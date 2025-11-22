from datetime import datetime
from src.connectors.mysql_connector import MySQLConnector
from src.connectors.mongodb_connector import MongoDBConnector
from src.transformers.game_transformer import GameTransformer
from src.transformers.user_transformer import UserTransformer
from src.transformers.matchup_transformer import MatchupTransformer
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MySQLToMongoDBMigration:
    def __init__(self):
        self.mysql_conn = None
        self.mongodb_conn = None
        self._setup_connections()
    
    def _setup_connections(self):
        try:
            self.mysql_conn = MySQLConnector()
            self.mongodb_conn = MongoDBConnector()
        except Exception as e:
            logger.error(f"Failed to setup connections: {e}")
            self.close_connections()
            raise
    
    @staticmethod
    def _serialize_datetime(dt_obj):
        """Convert datetime to ISO format string"""
        if dt_obj is None:
            return None
        if isinstance(dt_obj, datetime):
            return dt_obj.isoformat()
        return dt_obj
    
    def migrate_games(self):
        """Migrate games with nested data"""
        if not getattr(settings, 'MIGRATE_GAMES', True):
            logger.info("Skipping games migration")
            return
        
        logger.info("Starting games migration")
        self.mongodb_conn.delete_collection('games')
        
        try:
            games_data = self.mysql_conn.get_complete_game_data()
            
            for game in games_data:
                try:
                    reviews = self.mysql_conn.get_game_reviews(game['id'])
                    
                    for review in reviews:
                        review['comments'] = self.mysql_conn.get_review_comments(review['id'])
                    
                    designers = []
                    if game['designer_ids']:
                        designer_ids = game['designer_ids'].split(',')
                        designer_names = game['designer_names'].split(',')
                        designers = [{'id': int(did), 'name': name} 
                                   for did, name in zip(designer_ids, designer_names)]
                    
                    artists = []
                    if game['artist_ids']:
                        artist_ids = game['artist_ids'].split(',')
                        artist_names = game['artist_names'].split(',')
                        artists = [{'id': int(aid), 'name': name} 
                                 for aid, name in zip(artist_ids, artist_names)]
                    
                    genres = []
                    if game['genre_ids']:
                        genre_ids = game['genre_ids'].split(',')
                        genre_titles = game['genre_titles'].split(',')
                        genres = [{'id': int(gid), 'title': title} 
                                for gid, title in zip(genre_ids, genre_titles)]
                    
                    game_document = GameTransformer.transform_game_data(
                        game, designers, artists, genres, reviews
                    )
                    game_document['metadata']['migrated_at'] = self._serialize_datetime(datetime.utcnow())
                    
                    self.mongodb_conn.insert_documents('games', [game_document])
                    logger.info(f"Migrated game: {game['name']} (ID: {game['id']})")
                    
                except Exception as e:
                    logger.error(f"Error migrating game {game['id']}: {e}")
                    continue
            
            logger.info("Games migration completed")
            
        except Exception as e:
            logger.error(f"Error in games migration: {e}")
            raise
    
    def migrate_users(self):
        """Migrate users with nested social data"""
        if not getattr(settings, 'MIGRATE_USERS', True):
            logger.info("Skipping users migration")
            return
        
        logger.info("Starting users migration")
        self.mongodb_conn.delete_collection('users')
        
        try:
            users_data = self.mysql_conn.get_complete_user_data()
            
            for user in users_data:
                try:
                    friendships = self.mysql_conn.get_user_friendships(user['id'])
                    messages = self.mysql_conn.get_user_messages(user['id'])
                    
                    sent_messages = [msg for msg in messages if msg['user_id_1'] == user['id']]
                    received_messages = [msg for msg in messages if msg['user_id_2'] == user['id']]
                    
                    user_document = UserTransformer.transform_user_data(
                        user, friendships, sent_messages, received_messages
                    )
                    user_document['metadata']['migrated_at'] = self._serialize_datetime(datetime.utcnow())
                    
                    self.mongodb_conn.insert_documents('users', [user_document])
                    logger.info(f"Migrated user: {user['display_name']} (ID: {user['id']})")
                    
                except Exception as e:
                    logger.error(f"Error migrating user {user['id']}: {e}")
                    continue
            
            logger.info("Users migration completed")
            
        except Exception as e:
            logger.error(f"Error in users migration: {e}")
            raise
    
    def migrate_matchups(self):
        """Migrate matchups with complete game sessions"""
        if not getattr(settings, 'MIGRATE_MATCHUPS', True):
            logger.info("Skipping matchups migration")
            return
        
        logger.info("Starting matchups migration")
        self.mongodb_conn.delete_collection('matchups')
        
        try:
            matchups_data = self.mysql_conn.get_complete_matchup_data()
            
            for matchup in matchups_data:
                try:
                    moves = self.mysql_conn.get_matchup_moves(matchup['id'])
                    comments = self.mysql_conn.get_matchup_comments(matchup['id'])
                    spectators = self.mysql_conn.get_matchup_spectators(matchup['id'])
                    
                    player_ids = [matchup['user_id_1'], matchup['user_id_2'], matchup['user_id_winner'], matchup['created_by_user_id']]
                    players = self.mysql_conn.get_complete_user_data()
                    relevant_players = [p for p in players if p['id'] in player_ids]
                    
                    game_data = self.mysql_conn.get_complete_game_data(matchup['game_id'])
                    game_info = game_data[0] if game_data else None
                    
                    matchup_document = MatchupTransformer.transform_matchup_data(
                        matchup, relevant_players, moves, comments, spectators, game_info
                    )
                    matchup_document['metadata']['migrated_at'] = self._serialize_datetime(datetime.utcnow())
                    
                    self.mongodb_conn.insert_documents('matchups', [matchup_document])
                    logger.info(f"Migrated matchup: {matchup['id']}")
                    
                except Exception as e:
                    logger.error(f"Error migrating matchup {matchup['id']}: {e}")
                    continue
            
            logger.info("Matchups migration completed")
            
        except Exception as e:
            logger.error(f"Error in matchups migration: {e}")
            raise
    
    def migrate_all(self):
        """Run all migrations"""
        logger.info("Starting complete migration from MySQL to MongoDB")
        
        try:
            self.migrate_games()
            self.migrate_users()
            self.migrate_matchups()
            
            logger.info("All migrations completed successfully")
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            raise
        finally:
            self.close_connections()
    
    def close_connections(self):
        if self.mysql_conn:
            self.mysql_conn.close()
        if self.mongodb_conn:
            self.mongodb_conn.close()