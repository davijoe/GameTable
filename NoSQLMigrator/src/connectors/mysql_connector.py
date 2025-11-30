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
            GROUP_CONCAT(DISTINCT gen.title) as genre_titles
        FROM game g
        LEFT JOIN game_designers gd ON g.id = gd.game_id
        LEFT JOIN designer d ON gd.designer_id = d.id
        LEFT JOIN game_artists ga ON g.id = ga.game_id
        LEFT JOIN artists a ON ga.artists_id = a.id
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
        SELECT r.*, u.display_name 
        FROM review r
        JOIN game_reviews gr ON r.id = gr.review_id
        JOIN user u ON r.user_id = u.id
        WHERE gr.game_id = %s
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (game_id,))
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
    
    def get_user_friendships(self, user_id):
        """Get all friendships for a user"""
        query = """
        SELECT * FROM friendship 
        WHERE user_id_1 = %s OR user_id_2 = %s
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (user_id, user_id))
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def get_user_messages(self, user_id):
        """Get all messages for a user"""
        query = """
        SELECT * FROM message 
        WHERE user_id_1 = %s OR user_id_2 = %s
        ORDER BY timestamp
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (user_id, user_id))
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def get_complete_matchup_data(self, matchup_id=None):
        """Get complete matchup data with all related entities"""
        query = "SELECT * FROM matchup"
        params = None
        
        if matchup_id:
            query += " WHERE id = %s"
            params = (matchup_id,)
        
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def get_matchup_moves(self, matchup_id):
        """Get all moves for a matchup"""
        query = """
        SELECT m.* FROM move m
        JOIN matchup_move mm ON m.id = mm.move_id
        WHERE mm.matchup_id = %s
        ORDER BY m.ply
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (matchup_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def get_matchup_comments(self, matchup_id):
        """Get all comments for a matchup"""
        query = "SELECT * FROM matchup_comments WHERE matchup_id = %s"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (matchup_id,))
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def get_matchup_spectators(self, matchup_id):
        """Get all spectators for a matchup"""
        query = """
        SELECT u.id as user_id, u.display_name 
        FROM spectator s
        JOIN spectator_users su ON s.id = su.spectator_id
        JOIN user u ON su.user_id = u.id
        WHERE s.matchup_id = %s
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, (matchup_id,))
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
        query = "SELECT * FROM artists"
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

    def get_all_friendships(self):
        """Get all friendships"""
        query = "SELECT * FROM friendship"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_messages(self):
        """Get all messages"""
        query = "SELECT * FROM message"
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

    def get_all_game_reviews(self):
        """Get all game-review relationships"""
        query = "SELECT * FROM game_reviews"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_moves(self):
        """Get all moves"""
        query = "SELECT * FROM move"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_matchup_moves(self):
        """Get all matchup-move relationships"""
        query = "SELECT * FROM matchup_move"
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_all_spectators_with_users(self):
        """Get all spectators with user information"""
        query = """
        SELECT s.id as spectator_id, s.matchup_id, su.user_id, u.display_name
        FROM spectator s
        JOIN spectator_users su ON s.id = su.spectator_id
        JOIN user u ON su.user_id = u.id
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL connection closed")