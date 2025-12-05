from src.utils.logger import get_logger

logger = get_logger(__name__)

class GameTransformer:
    @staticmethod
    def transform_game_data(game_data, designers, artists, genres, publishers, mechanics, videos, review_ids):
        """Transform flat game data into nested MongoDB document"""
        
        avg_rating = 0 
        total_reviews = len(review_ids)
        
        game_document = {
            '_id': game_data['id'],
            'name': game_data['name'],
            'slug': game_data['slug'],
            'year_published': game_data['year_published'],
            'ratings': {
                'bgg_rating': game_data['bgg_rating'],
                'difficulty_rating': game_data['difficulty_rating'],
                'average_user_rating': avg_rating, 
                'total_reviews': total_reviews
            },
            'description': game_data['description'],
            'playing_time': game_data['playing_time'],
            'player_count': {
                'min': game_data['min_players'],
                'max': game_data['max_players']
            },
            'minimum_age': game_data['minimum_age'],
            'images': {
                'thumbnail': game_data['thumbnail'],
                'image': game_data['image']
            },
            'designers': designers,
            'artists': artists,
            'genres': genres,
            'publishers': publishers,
            'mechanics': mechanics,
            'videos': videos,
            'review_ids': review_ids,
            'metadata': {
                'source_id': game_data['id'],
                'migrated_at': None
            }
        }
        
        return game_document