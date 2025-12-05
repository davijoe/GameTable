from src.utils.logger import get_logger
from datetime import datetime, date 

logger = get_logger(__name__)

class ReviewTransformer:
    @staticmethod
    def transform_review_data(review_data, user_info, game_ids):
        """Transform review data into MongoDB document"""
        review_doc = {
            '_id': review_data['id'],
            'title': review_data['title'],
            'text': review_data['text'],
            'star_amount': review_data['star_amount'],
            'user': {
                'id': review_data['user_id'],
                'display_name': user_info.get('display_name'),
                'username': user_info.get('username')
            },
            'games': game_ids,
            'metadata': {
                'source_id': review_data['id'],
                'created_at': ReviewTransformer._serialize_date(review_data.get('created_at')),
                'updated_at': ReviewTransformer._serialize_date(review_data.get('updated_at')),
                'migrated_at': None
            }
        }
        return review_doc
    
    @staticmethod
    def _serialize_date(date_obj):
        """Convert date/datetime objects to ISO format string"""
        if date_obj is None:
            return None
        if isinstance(date_obj, datetime):
            return date_obj.isoformat()
        if isinstance(date_obj, date):
            return date_obj.isoformat()
        return str(date_obj)