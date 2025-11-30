from src.utils.logger import get_logger

logger = get_logger(__name__)

class Neo4jTransformer:
    @staticmethod
    def create_user_nodes(users_data):
        """Create User nodes with properties"""
        queries = []
        for user in users_data:
            query = """
            CREATE (u:User {
                id: $id,
                display_name: $display_name,
                username: $username,
                email: $email,
                dob: $dob,
                migrated_at: datetime()
            })
            """
            queries.append({
                'query': query,
                'params': {
                    'id': user['id'],
                    'display_name': user['display_name'],
                    'username': user['username'],
                    'email': user['email'],
                    'dob': user['dob']
                }
            })
        return queries

    @staticmethod
    def create_game_nodes(games_data):
        """Create Game nodes with properties"""
        queries = []
        for game in games_data:
            query = """
            CREATE (g:Game {
                id: $id,
                name: $name,
                slug: $slug,
                year_published: $year_published,
                bgg_rating: $bgg_rating,
                difficulty_rating: $difficulty_rating,
                description: $description,
                play_time: $play_time,
                available: $available,
                min_players: $min_players,
                max_players: $max_players,
                migrated_at: datetime()
            })
            """
            queries.append({
                'query': query,
                'params': {
                    'id': game['id'],
                    'name': game['name'],
                    'slug': game['slug'],
                    'year_published': game['year_published'],
                    'bgg_rating': float(game['bgg_rating']) if game['bgg_rating'] else 0.0,
                    'difficulty_rating': float(game['difficulty_rating']) if game['difficulty_rating'] else 0.0,
                    'description': game['description'],
                    'play_time': game['play_time'],
                    'available': bool(game['available']),
                    'min_players': game['min_players'],
                    'max_players': game['max_players']
                }
            })
        return queries

    @staticmethod
    def create_designer_artist_nodes(designers_data, artists_data):
        """Create Designer and Artist nodes"""
        queries = []
        
        for designer in designers_data:
            query = """
            CREATE (d:Designer {
                id: $id,
                name: $name,
                dob: $dob,
                migrated_at: datetime()
            })
            """
            queries.append({
                'query': query,
                'params': {
                    'id': designer['id'],
                    'name': designer['name'],
                    'dob': designer['dob']
                }
            })
        
        for artist in artists_data:
            query = """
            CREATE (a:Artist {
                id: $id,
                name: $name,
                dob: $dob,
                migrated_at: datetime()
            })
            """
            queries.append({
                'query': query,
                'params': {
                    'id': artist['id'],
                    'name': artist['name'],
                    'dob': artist['dob']
                }
            })
        
        return queries

    @staticmethod
    def create_genre_nodes(genres_data):
        """Create Genre nodes"""
        queries = []
        for genre in genres_data:
            query = """
            CREATE (gen:Genre {
                id: $id,
                title: $title,
                description: $description,
                migrated_at: datetime()
            })
            """
            queries.append({
                'query': query,
                'params': {
                    'id': genre['id'],
                    'title': genre['title'],
                    'description': genre['description']
                }
            })
        return queries

    @staticmethod
    def create_game_relationships(game_designers, game_artists, game_genres):
        """Create relationships between games and designers/artists/genres"""
        queries = []
        
        for gd in game_designers:
            query = """
            MATCH (g:Game {id: $game_id}), (d:Designer {id: $designer_id})
            CREATE (g)-[:DESIGNED_BY]->(d)
            """
            queries.append({
                'query': query,
                'params': {
                    'game_id': gd['game_id'],
                    'designer_id': gd['designer_id']
                }
            })
        
        for ga in game_artists:
            query = """
            MATCH (g:Game {id: $game_id}), (a:Artist {id: $artist_id})
            CREATE (g)-[:ART_BY]->(a)
            """
            queries.append({
                'query': query,
                'params': {
                    'game_id': ga['game_id'],
                    'artist_id': ga['artists_id']
                }
            })
        
        for gg in game_genres:
            query = """
            MATCH (g:Game {id: $game_id}), (gen:Genre {id: $genre_id})
            CREATE (g)-[:IN_GENRE]->(gen)
            """
            queries.append({
                'query': query,
                'params': {
                    'game_id': gg['game_id'],
                    'genre_id': gg['genre_id']
                }
            })
        
        return queries

    @staticmethod
    def create_friendship_relationships(friendships_data):
        """Create FRIENDS_WITH relationships between users"""
        queries = []
        for friendship in friendships_data:
            query = """
            MATCH (u1:User {id: $user1_id}), (u2:User {id: $user2_id})
            CREATE (u1)-[f:FRIENDS_WITH {
                status: $status,
                created_at: $created_at,
                updated_at: $updated_at
            }]->(u2)
            """
            queries.append({
                'query': query,
                'params': {
                    'user1_id': friendship['user_id_1'],
                    'user2_id': friendship['user_id_2'],
                    'status': friendship['status'],
                    'created_at': friendship['created_at'],
                    'updated_at': friendship['updated_at']
                }
            })
        return queries

    @staticmethod
    def create_matchup_nodes_and_relationships(matchups_data, players_data, games_data):
        """Create Matchup nodes and relationships with players and games"""
        queries = []
        
        for matchup in matchups_data:
            matchup_query = """
            CREATE (m:Matchup {
                id: $id,
                start_time: $start_time,
                end_time: $end_time,
                created_at: $created_at,
                is_private: $is_private,
                is_expired: $is_expired,
                migrated_at: datetime()
            })
            """
            queries.append({
                'query': matchup_query,
                'params': {
                    'id': matchup['id'],
                    'start_time': matchup['start_time'],
                    'end_time': matchup['end_time'],
                    'created_at': matchup['created_at'],
                    'is_private': bool(matchup['is_private']),
                    'is_expired': bool(matchup.get('is_expired', 0))
                }
            })
            
            game_rel_query = """
            MATCH (m:Matchup {id: $matchup_id}), (g:Game {id: $game_id})
            CREATE (m)-[:PLAYED]->(g)
            """
            queries.append({
                'query': game_rel_query,
                'params': {
                    'matchup_id': matchup['id'],
                    'game_id': matchup['game_id']
                }
            })
            
            player_queries = Neo4jTransformer._create_player_relationships(matchup, players_data)
            queries.extend(player_queries)
        
        return queries

    @staticmethod
    def _create_player_relationships(matchup, players_data):
        """Create relationships between matchups and players"""
        queries = []
        
        queries.append({
            'query': """
            MATCH (m:Matchup {id: $matchup_id}), (u:User {id: $user_id})
            CREATE (u)-[:PARTICIPATED_IN {role: 'PLAYER1'}]->(m)
            """,
            'params': {
                'matchup_id': matchup['id'],
                'user_id': matchup['user_id_1']
            }
        })
        
        queries.append({
            'query': """
            MATCH (m:Matchup {id: $matchup_id}), (u:User {id: $user_id})
            CREATE (u)-[:PARTICIPATED_IN {role: 'PLAYER2'}]->(m)
            """,
            'params': {
                'matchup_id': matchup['id'],
                'user_id': matchup['user_id_2']
            }
        })
        
        if matchup['user_id_winner'] and matchup['user_id_winner'] != 0:
            queries.append({
                'query': """
                MATCH (m:Matchup {id: $matchup_id}), (u:User {id: $user_id})
                CREATE (u)-[:WON]->(m)
                """,
                'params': {
                    'matchup_id': matchup['id'],
                    'user_id': matchup['user_id_winner']
                }
            })
        
        if matchup['created_by_user_id']:
            queries.append({
                'query': """
                MATCH (m:Matchup {id: $matchup_id}), (u:User {id: $user_id})
                CREATE (u)-[:CREATED]->(m)
                """,
                'params': {
                    'matchup_id': matchup['id'],
                    'user_id': matchup['created_by_user_id']
                }
            })
        
        return queries

    @staticmethod
    def create_review_nodes_and_relationships(reviews_data, users_data, games_data):
        """Create Review nodes and relationships"""
        queries = []
        
        for review in reviews_data:
            review_query = """
            CREATE (r:Review {
                id: $id,
                title: $title,
                text: $text,
                star_amount: $star_amount,
                migrated_at: datetime()
            })
            """
            queries.append({
                'query': review_query,
                'params': {
                    'id': review['id'],
                    'title': review['title'],
                    'text': review['text'],
                    'star_amount': review['star_amount']
                }
            })
            
            queries.append({
                'query': """
                MATCH (r:Review {id: $review_id}), (u:User {id: $user_id})
                CREATE (u)-[:WROTE]->(r)
                """,
                'params': {
                    'review_id': review['id'],
                    'user_id': review['user_id']
                }
            })
            
        
        return queries

    @staticmethod
    def create_game_review_relationships(game_reviews_data):
        """Create relationships between games and reviews"""
        queries = []
        for gr in game_reviews_data:
            query = """
            MATCH (g:Game {id: $game_id}), (r:Review {id: $review_id})
            CREATE (r)-[:FOR_GAME]->(g)
            """
            queries.append({
                'query': query,
                'params': {
                    'game_id': gr['game_id'],
                    'review_id': gr['review_id']
                }
            })
        return queries

    @staticmethod
    def create_message_relationships(messages_data):
        """Create MESSAGED relationships between users"""
        queries = []
        for message in messages_data:
            query = """
            MATCH (u1:User {id: $from_user_id}), (u2:User {id: $to_user_id})
            CREATE (u1)-[msg:MESSAGED {
                text: $text,
                timestamp: $timestamp
            }]->(u2)
            """
            queries.append({
                'query': query,
                'params': {
                    'from_user_id': message['user_id_1'],
                    'to_user_id': message['user_id_2'],
                    'text': message['text'],
                    'timestamp': message['timestamp']
                }
            })
        return queries

    @staticmethod
    def create_spectator_relationships(spectators_data):
        """Create SPECTATED relationships"""
        queries = []
        for spectator in spectators_data:
            query = """
            MATCH (u:User {id: $user_id}), (m:Matchup {id: $matchup_id})
            CREATE (u)-[:SPECTATED]->(m)
            """
            queries.append({
                'query': query,
                'params': {
                    'user_id': spectator['user_id'],
                    'matchup_id': spectator['matchup_id']
                }
            })
        return queries

    @staticmethod
    def create_move_nodes_and_relationships(moves_data, matchup_moves_data):
        """Create Move nodes and relationships with matchups"""
        queries = []
        
        for move in moves_data:
            # Create Move node
            move_query = """
            CREATE (mv:Move {
                id: $id,
                ply: $ply,
                start_x: $start_x,
                start_y: $start_y,
                end_x: $end_x,
                end_y: $end_y,
                migrated_at: datetime()
            })
            """
            queries.append({
                'query': move_query,
                'params': {
                    'id': move['id'],
                    'ply': move['ply'],
                    'start_x': move['start_x_coordinate'],
                    'start_y': move['start_y_coordinate'],
                    'end_x': move['end_x_coordinate'],
                    'end_y': move['end_y_coordinate']
                }
            })
        
        # Create matchup-move relationships
        for mm in matchup_moves_data:
            query = """
            MATCH (m:Matchup {id: $matchup_id}), (mv:Move {id: $move_id})
            CREATE (m)-[:CONTAINS_MOVE {order: mv.ply}]->(mv)
            """
            queries.append({
                'query': query,
                'params': {
                    'matchup_id': mm['matchup_id'],
                    'move_id': mm['move_id']
                }
            })
        
        return queries