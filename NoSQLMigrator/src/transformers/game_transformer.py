from src.utils.logger import get_logger

logger = get_logger(__name__)

class GameTransformer:
    @staticmethod
    def transform_game_data(game_data, designers, artists, genres, reviews):
        """Transform flat game data into nested MongoDB document"""
        
        transformed_reviews = []
        for review in reviews:
            transformed_review = {
                'id': review['id'],
                'title': review['title'],
                'text': review['text'],
                'star_amount': review['star_amount'],
                'user_id': review['user_id'],
                'comments': []  
            }
            transformed_reviews.append(transformed_review)
        
        avg_rating = sum(review['star_amount'] for review in reviews) / len(reviews) if reviews else 0
        
        game_document = {
            '_id': game_data['id'],
            'name': game_data['name'],
            'slug': game_data['slug'],
            'year_published': game_data['year_published'],
            'ratings': {
                'bgg_rating': game_data['bgg_rating'],
                'difficulty_rating': game_data['difficulty_rating'],
                'average_user_rating': avg_rating,
                'total_reviews': len(reviews)
            },
            'description': game_data['description'],
            'play_time': game_data['play_time'],
            'available': bool(game_data['available']),
            'player_count': {
                'min': game_data['min_players'],
                'max': game_data['max_players']
            },
            'designers': designers,
            'artists': artists,
            'genres': genres,
            'reviews': transformed_reviews,
            'metadata': {
                'source_id': game_data['id'],
                'migrated_at': None
            }
        }
        
        return game_document
    
    @staticmethod
    def transform_review_comments(comments_data):
        """Transform review comments into nested structure"""
        transformed_comments = []
        for comment in comments_data:
            transformed_comment = {
                'id': comment['id'],
                'text': comment['text'],
                'user_id': comment['user_id'],
                'created_at': comment['created_at'],
                'updated_at': comment['updated_at']
            }
            transformed_comments.append(transformed_comment)
        return transformed_comments