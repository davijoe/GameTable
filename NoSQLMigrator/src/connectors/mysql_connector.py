import mysql.connector
from mysql.connector import Error
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MySQLConnector:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                database=settings.MYSQL_DATABASE,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                charset='utf8mb4'
            )
            logger.info("Connected to MySQL successfully")
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            raise
    
    def get_complete_game_data(self, game_id=None):
        """Get complete game data with all related entities"""
        query = """
        SELECT 
            g.*,
            GROUP_CONCAT(DISTINCT d.id) as designer_ids,
            GROUP_CONCAT(DISTINCT d.name) as designer_names,
            GROUP_CONCAT(DISTINCT a.id) as artist_ids,
            GROUP_CONCAT(DISTINCT a.name) as artist_names,
            GROUP_CONCAT(DISTINCT gen.id) as genre_ids,
            GROUP_CONCAT(DISTINCT gen.name) as genre_names
        FROM game g
        LEFT JOIN game_designers gd ON g.id = gd.game_id
        LEFT JOIN designer d ON gd.designer_id = d.id
        LEFT JOIN game_artists ga ON g.id = ga.game_id
        LEFT JOIN artist a ON ga.artist_id = a.id
        LEFT JOIN game_genres gg ON g.id = gg.game_id
        LEFT JOIN genre gen ON gg.genre_id = gen.id
        """
        
        if game_id:
            query += " WHERE g.id = %s"
            params = (game_id,)
        else:
            params = None
            
        query += " GROUP BY g.id"
        
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
        
    def get_game_reviews(self, game_id):
        """Get all reviews for a game"""
        query = """
        SELECT r.*, u.display_name, u.username
        FROM review r
        JOIN user u ON r.user_id = u.id
        WHERE r.game_id = %s  -- Direct filter on game_id, no junction table
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (game_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def get_game_reviews_with_users(self, game_id, limit=None):
        """Get reviews for a game with user information"""
        query = """
        SELECT r.*, u.display_name
        FROM review r
        JOIN game_reviews gr ON r.id = gr.review_id
        JOIN user u ON r.user_id = u.id
        WHERE gr.game_id = %s
        """
        
        if limit:
            query += " LIMIT %s"
            params = (game_id, limit)
        else:
            params = (game_id,)
        
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
            
    def get_review_comments(self, review_id):
        """Get comments for a review"""
        query = "SELECT * FROM review_comments WHERE review_id = %s"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (review_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def get_complete_user_data(self, user_id=None):
        """Get user data with friendships and messages"""
        query = "SELECT * FROM user"
        params = None
        
        if user_id:
            query += " WHERE id = %s"
            params = (user_id,)
        
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_designers(self):
        """Get all designers"""
        query = "SELECT * FROM designer"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_artists(self):
        """Get all artists"""
        query = "SELECT * FROM artist"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_genres(self):
        """Get all genres"""
        query = "SELECT * FROM genre"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_game_designers(self):
        """Get all game-designer relationships"""
        query = "SELECT * FROM game_designers"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_game_artists(self):
        """Get all game-artist relationships"""
        query = "SELECT * FROM game_artists"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_game_genres(self):
        """Get all game-genre relationships"""
        query = "SELECT * FROM game_genres"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_reviews(self):
        """Get all reviews"""
        query = "SELECT * FROM review"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_publishers(self):
        """Get all publishers"""
        query = "SELECT * FROM publisher"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_mechanics(self):
        """Get all mechanics"""
        query = "SELECT * FROM mechanic"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_languages(self):
        """Get all languages"""
        query = "SELECT * FROM language"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_videos(self):
        """Get all videos"""
        query = "SELECT * FROM video"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_game_publishers(self):
        """Get all game-publisher relationships"""
        query = "SELECT * FROM game_publishers"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_game_mechanics(self):
        """Get all game-mechanic relationships"""
        query = "SELECT * FROM game_mechanics"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_game_publishers(self, game_id):
        """Get publishers for a specific game"""
        query = """
        SELECT p.* 
        FROM publisher p
        JOIN game_publishers gp ON p.id = gp.publisher_id
        WHERE gp.game_id = %s
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (game_id,))
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_game_mechanics(self, game_id):
        """Get mechanics for a specific game"""
        query = """
        SELECT m.* 
        FROM mechanic m
        JOIN game_mechanics gm ON m.id = gm.mechanic_id
        WHERE gm.game_id = %s
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (game_id,))
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_game_videos(self, game_id):
        """Get videos for a specific game"""
        query = """
        SELECT v.*, l.language 
        FROM video v
        JOIN language l ON v.language_id = l.id
        WHERE v.game_id = %s
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (game_id,))
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_reviews_with_user_info(self, game_id=None):
        """Get reviews with user information"""
        query = """
        SELECT r.*, u.display_name, u.username
        FROM review r
        JOIN user u ON r.user_id = u.id
        """
        
        if game_id:
            query += " WHERE r.game_id = %s"
            params = (game_id,)
        else:
            params = None
            
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
        
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection closed")