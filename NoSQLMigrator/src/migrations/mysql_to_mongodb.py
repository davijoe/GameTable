from datetime import datetime, date 
from src.connectors.mysql_connector import MySQLConnector
from src.connectors.mongodb_connector import MongoDBConnector
from src.transformers.game_transformer import GameTransformer
from src.transformers.user_transformer import UserTransformer
from src.transformers.review_transformer import ReviewTransformer
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
    def _serialize_date(date_obj):
        """Convert date/datetime objects to ISO format string or None"""
        if date_obj is None:
            return None
        if isinstance(date_obj, datetime):
            return date_obj.isoformat()
        if isinstance(date_obj, date):
            return date_obj.isoformat()
        return str(date_obj)

    @staticmethod
    def _serialize_datetime(dt_obj):
        """Convert datetime to ISO format string"""
        if dt_obj is None:
            return None
        if isinstance(dt_obj, datetime):
            return dt_obj.isoformat()
        if isinstance(dt_obj, date):
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
            
            logger.info("Collecting review IDs for all games...")
            reviews_by_game = {}
            all_reviews = self.mysql_conn.get_reviews_with_user_info()
            
            for review in all_reviews:
                game_id = review['game_id']
                if game_id not in reviews_by_game:
                    reviews_by_game[game_id] = []
                reviews_by_game[game_id].append(review['id'])
            
            logger.info(f"Collected reviews for {len(reviews_by_game)} games")
            
            for game in games_data:
                try:
                    game_id = game['id']
                    
                    review_ids = reviews_by_game.get(game_id, [])
                    
                    designers = self._get_game_designers(game)
                    artists = self._get_game_artists(game)
                    genres = self._get_game_genres(game)
                    publishers = self.mysql_conn.get_game_publishers(game_id)
                    mechanics = self.mysql_conn.get_game_mechanics(game_id)
                    videos = self.mysql_conn.get_game_videos(game_id)
                    
                    publisher_list = [{'id': p['id'], 'name': p['name']} for p in publishers]
                    mechanic_list = [{'id': m['id'], 'name': m['name']} for m in mechanics]
                    
                    video_list = []
                    for video in videos:
                        video_data = {
                            'id': video['id'],
                            'title': video['title'],
                            'category': video['category'],
                            'link': video['link'],
                            'language': video['language']
                        }
                        video_list.append(video_data)
                    
                    game_document = GameTransformer.transform_game_data(
                        game, designers, artists, genres, publisher_list, 
                        mechanic_list, video_list, review_ids
                    )
                    game_document['metadata']['migrated_at'] = self._serialize_datetime(datetime.utcnow())
                    
                    self.mongodb_conn.insert_documents('games', [game_document])
                    logger.info(f"Migrated game: {game['name']} (ID: {game_id}, Reviews: {len(review_ids)})")
                    
                except Exception as e:
                    logger.error(f"Error migrating game {game.get('id', 'unknown')}: {e}")
                    continue
            
            logger.info("Games migration completed")
            
        except Exception as e:
            logger.error(f"Error in games migration: {e}")
            raise
    
    def migrate_reviews(self):
        """Migrate reviews to separate collection - now with direct game_id"""
        if not getattr(settings, 'MIGRATE_REVIEWS', True):
            logger.info("Skipping reviews migration")
            return
        
        logger.info("Starting reviews migration")
        self.mongodb_conn.delete_collection('reviews')
        
        try:
            reviews = self.mysql_conn.get_reviews_with_user_info()
            
            users_data = {}
            all_users = self.mysql_conn.get_complete_user_data()
            for user in all_users:
                users_data[user['id']] = {
                    'display_name': user['display_name'],
                    'username': user['username']
                }
            
            review_documents = []
            
            for review in reviews:
                try:
                    game_id = review['game_id']
                    
                    user_id = review['user_id']
                    user_info = users_data.get(user_id, {})
                    
                    review_doc = ReviewTransformer.transform_review_data(
                        review, user_info, game_id
                    )
                    review_doc['metadata']['migrated_at'] = self._serialize_datetime(datetime.utcnow())
                    
                    review_documents.append(review_doc)
                    
                    if len(review_documents) >= 1000:
                        self.mongodb_conn.insert_documents('reviews', review_documents)
                        logger.info(f"Migrated batch of {len(review_documents)} reviews")
                        review_documents = []
                        
                except Exception as e:
                    logger.error(f"Error migrating review {review.get('id', 'unknown')}: {e}")
                    continue
            
            if review_documents:
                self.mongodb_conn.insert_documents('reviews', review_documents)
                logger.info(f"Migrated final batch of {len(review_documents)} reviews")
            
            logger.info(f"Completed reviews migration")
            
        except Exception as e:
            logger.error(f"Error in reviews migration: {e}")
            raise
    
    def _get_game_designers(self, game):
        """Extract designers from game data"""
        designers = []
        if game.get('designer_ids'):
            designer_ids = game['designer_ids'].split(',')
            designer_names = game['designer_names'].split(',')
            designers = [{'id': int(did), 'name': name} 
                    for did, name in zip(designer_ids, designer_names)]
        return designers

    def _get_game_artists(self, game):
        """Extract artists from game data"""
        artists = []
        if game.get('artist_ids'):
            artist_ids = game['artist_ids'].split(',')
            artist_names = game['artist_names'].split(',')
            artists = [{'id': int(aid), 'name': name} 
                    for aid, name in zip(artist_ids, artist_names)]
        return artists

    def _get_game_genres(self, game):
        """Extract genres from game data"""
        genres = []
        if game.get('genre_ids'):
            genre_ids = game['genre_ids'].split(',')
            genre_names = game['genre_names'].split(',')
            genres = [{'id': int(gid), 'name': name} 
                    for gid, name in zip(genre_ids, genre_names)]
        return genres

    def migrate_users(self):
        """Migrate users"""
        if not getattr(settings, 'MIGRATE_USERS', True):
            logger.info("Skipping users migration")
            return
        
        logger.info("Starting users migration")
        self.mongodb_conn.delete_collection('users')
        
        try:
            users_data = self.mysql_conn.get_complete_user_data()
            user_documents = []
            
            for user in users_data:
                user_doc = {
                    '_id': user['id'],
                    'display_name': user['display_name'],
                    'username': user['username'],
                    'email': user['email'],
                    'dob': self._serialize_date(user['dob']),
                    'metadata': {
                        'source_id': user['id'],
                        'migrated_at': self._serialize_datetime(datetime.utcnow())
                    }
                }
                user_documents.append(user_doc)
            
            if user_documents:
                self.mongodb_conn.insert_documents('users', user_documents)
                logger.info(f"Migrated {len(user_documents)} users")
            
        except Exception as e:
            logger.error(f"Error in users migration: {e}")
            raise
        
    def _update_game_ratings(self):
        """Update average ratings in games based on reviews"""
        logger.info("Updating game average ratings based on reviews...")
        
        try:
            pipeline = [
                {"$group": {
                    "_id": "$game_id",
                    "avg_rating": {"$avg": "$star_amount"}
                }}
            ]
            
            collection = self.mongodb_conn.db['reviews']
            results = list(collection.aggregate(pipeline))
            
            games_collection = self.mongodb_conn.db['games']
            
            for result in results:
                game_id = result['_id']
                avg_rating = result['avg_rating']
                
                games_collection.update_one(
                    {"_id": game_id},
                    {"$set": {
                        "ratings.average_user_rating": avg_rating
                    }}
                )
            
            logger.info(f"Updated average ratings for {len(results)} games")
            
        except Exception as e:
            logger.error(f"Error updating ratings: {e}")
    
    def migrate_all(self):
        """Run all migrations"""
        logger.info("Starting complete migration from MySQL to MongoDB")
        
        try:
            self.migrate_users()
            self.migrate_reviews()
            self.migrate_games()
            
            self._update_game_ratings()
            
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