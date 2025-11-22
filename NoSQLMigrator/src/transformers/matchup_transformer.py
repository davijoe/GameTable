from src.utils.logger import get_logger
from datetime import date, datetime

logger = get_logger(__name__)

class MatchupTransformer:
    @staticmethod
    def transform_matchup_data(matchup_data, players, moves, comments, spectators, game_data):
        """Transform matchup data into nested document"""
        
        player1 = next((p for p in players if p['id'] == matchup_data['user_id_1']), None)
        player2 = next((p for p in players if p['id'] == matchup_data['user_id_2']), None)
        winner = next((p for p in players if p['id'] == matchup_data['user_id_winner']), None)
        creator = next((p for p in players if p['id'] == matchup_data['created_by_user_id']), None)
        
        game_sequence = []
        for move in sorted(moves, key=lambda x: x['ply']):
            move_data = {
                'ply': move['ply'],
                'from': {
                    'x': move['start_x_coordinate'],
                    'y': move['start_y_coordinate']
                },
                'to': {
                    'x': move['end_x_coordinate'],
                    'y': move['end_y_coordinate']
                } if move['end_x_coordinate'] and move['end_y_coordinate'] else None,
                'move_id': move['id']
            }
            game_sequence.append(move_data)
        
        matchup_comments = []
        for comment in comments:
            comment_data = {
                'id': comment['id'],
                'user_id': comment['user_id'],
                'text': comment['text'],
                'timestamp': comment.get('created_at')
            }
            matchup_comments.append(comment_data)
        
        spectator_users = [s['user_id'] for s in spectators]
        
        matchup_document = {
            '_id': matchup_data['id'],
            'game': {
                'game_id': matchup_data['game_id'],
                'name': game_data.get('name', 'Unknown') if game_data else 'Unknown',
                'play_time': game_data.get('play_time', 0) if game_data else 0
            },
            'players': {
                'player1': {
                    'user_id': matchup_data['user_id_1'],
                    'display_name': player1['display_name'] if player1 else 'Unknown'
                },
                'player2': {
                    'user_id': matchup_data['user_id_2'],
                    'display_name': player2['display_name'] if player2 else 'Unknown'
                },
                'winner': {
                    'user_id': matchup_data['user_id_winner'],
                    'display_name': winner['display_name'] if winner else 'Unknown'
                } if matchup_data['user_id_winner'] else None
            },
            'timing': {
                'start_time': MatchupTransformer._serialize_date(matchup_data['start_time']),
                'end_time': MatchupTransformer._serialize_date(matchup_data['end_time']),
                'created_at': MatchupTransformer._serialize_date(matchup_data['created_at']),
                'duration_minutes': MatchupTransformer._calculate_duration(
                    matchup_data['start_time'], matchup_data['end_time']
                )
            },
            'settings': {
                'is_private': bool(matchup_data['is_private']),
                'is_expired': bool(matchup_data.get('is_expired', 0))
            },
            'game_sequence': game_sequence,
            'social': {
                'comments': [
                    {
                        'id': comment['id'],
                        'user_id': comment['user_id'],
                        'text': comment['text'],
                        'timestamp': MatchupTransformer._serialize_date(comment.get('created_at'))
                    }
                    for comment in comments
                ],
                'spectators': spectator_users,
                'spectator_count': len(spectator_users)
            },
            'metadata': {
                'created_by': creator['display_name'] if creator else 'Unknown',
                'created_by_user_id': matchup_data['created_by_user_id'],
                'total_moves': len(game_sequence),
                'source_id': matchup_data['id'],
                'migrated_at': None
            }
        }
        
        return matchup_document
    
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
    
    @staticmethod
    def _calculate_duration(start_time, end_time):
        """Calculate duration in minutes"""
        if not start_time or not end_time:
            return None
        
        try:
            duration = end_time - start_time
            return int(duration.total_seconds() / 60)
        except:
            return None