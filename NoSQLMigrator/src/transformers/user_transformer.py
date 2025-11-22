from src.utils.logger import get_logger
from datetime import date, datetime

logger = get_logger(__name__)

class UserTransformer:
    @staticmethod
    def transform_user_data(user_data, friendships, sent_messages, received_messages):
        """Transform user data into nested document with social connections"""
        
        friends = []
        for friendship in friendships:
            friend_id = friendship['user_id_2'] if friendship['user_id_1'] == user_data['id'] else friendship['user_id_1']
            friend_data = {
                'user_id': friend_id,
                'status': friendship['status'],
                'friends_since': UserTransformer._serialize_date(friendship['created_at']),
                'last_updated': UserTransformer._serialize_date(friendship['updated_at'])
            }
            friends.append(friend_data)
        
        conversations = UserTransformer._build_conversations(
            user_data['id'], sent_messages + received_messages
        )
        
        user_document = {
            '_id': user_data['id'],
            'display_name': user_data['display_name'],
            'username': user_data['username'],
            'profile': {
                'dob': UserTransformer._serialize_date(user_data['dob']),
                'email': user_data['email']
            },
            'social': {
                'friends': friends,
                'friend_count': len(friends),
                'conversations': conversations
            },
            'activity': {
                'reviews_written': 0,
                'matchups_played': 0,
                'games_owned': []
            },
            'metadata': {
                'source_id': user_data['id'],
                'migrated_at': None
            }
        }
        
        return user_document
    
    @staticmethod
    def _build_conversations(user_id, all_messages):
        """Build conversation threads from messages"""
        conversations = {}
        
        for message in all_messages:
            other_user_id = message['user_id_2'] if message['user_id_1'] == user_id else message['user_id_1']
            conversation_key = f"convo_{min(user_id, other_user_id)}_{max(user_id, other_user_id)}"
            
            if conversation_key not in conversations:
                conversations[conversation_key] = {
                    'participants': [user_id, other_user_id],
                    'messages': [],
                    'last_message': None,
                    '_last_message_timestamp': None
                }
            
            message_data = {
                'from_user_id': message['user_id_1'],
                'to_user_id': message['user_id_2'],
                'text': message['text'],
                'timestamp': UserTransformer._serialize_date(message['timestamp'])
            }
            
            conversations[conversation_key]['messages'].append(message_data)
            
            if (conversations[conversation_key]['_last_message_timestamp'] is None or 
                message['timestamp'] > conversations[conversation_key]['_last_message_timestamp']):
                conversations[conversation_key]['_last_message_timestamp'] = message['timestamp']
                conversations[conversation_key]['last_message'] = UserTransformer._serialize_date(message['timestamp'])
        
        conversation_list = list(conversations.values())
        conversation_list.sort(key=lambda x: x['_last_message_timestamp'] or datetime.min, reverse=True)
        
        for conv in conversation_list:
            del conv['_last_message_timestamp']
        
        return conversation_list
    
    @staticmethod
    def _serialize_date(date_obj):
        """Convert date/datetime objects to ISO format string"""
        if date_obj is None:
            return None
        if isinstance(date_obj, datetime):
            return date_obj.isoformat()
        if isinstance(date_obj, date):
            return date_obj.isoformat()
        return date_obj