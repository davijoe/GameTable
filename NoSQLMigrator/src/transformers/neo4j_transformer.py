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
                is_admin: $is_admin,
                migrated_at: datetime()
            })
            """
            query_dict = {
                "query": query,
                "params": {
                    "id": user["id"],
                    "display_name": user["display_name"],
                    "username": user["username"],
                    "email": user["email"],
                    "dob": user.get("dob"),
                    'is_admin': bool(user.get('is_admin', False))
                },
            }
            queries.append(query_dict)
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
                playing_time: $playing_time,
                min_players: $min_players,
                max_players: $max_players,
                thumbnail: $thumbnail,
                image: $image,
                migrated_at: datetime()
            })
            """
            queries.append(
                {
                    "query": query,
                    "params": {
                        "id": game["id"],
                        "name": game["name"],
                        "slug": game["slug"],
                        "year_published": game["year_published"],
                        "bgg_rating": float(game["bgg_rating"])
                        if game["bgg_rating"]
                        else 0.0,
                        "difficulty_rating": float(game["difficulty_rating"])
                        if game["difficulty_rating"]
                        else 0.0,
                        "description": game["description"],
                        "playing_time": game["playing_time"],
                        "min_players": game["min_players"],
                        "max_players": game["max_players"],
                        "thumbnail": game.get("thumbnail", ""),
                        "image": game.get("image", ""),
                    },
                }
            )
        return queries

    @staticmethod
    def create_publisher_nodes(publishers_data):
        """Create Publisher nodes"""
        queries = []
        for publisher in publishers_data:
            query = """
            CREATE (p:Publisher {
                id: $id,
                name: $name,
                migrated_at: datetime()
            })
            """
            queries.append(
                {
                    "query": query,
                    "params": {
                        "id": publisher["id"],
                        "name": publisher["name"],
                    },
                }
            )
        return queries

    @staticmethod
    def create_mechanic_nodes(mechanics_data):
        """Create Mechanic nodes"""
        queries = []
        for mechanic in mechanics_data:
            query = """
            CREATE (m:Mechanic {
                id: $id,
                name: $name,
                migrated_at: datetime()
            })
            """
            queries.append(
                {
                    "query": query,
                    "params": {"id": mechanic["id"], "name": mechanic["name"]},
                }
            )
        return queries

    @staticmethod
    def create_designer_nodes(designers_data):
        """Create Designer nodes"""
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
            queries.append(
                {
                    "query": query,
                    "params": {
                        "id": designer["id"],
                        "name": designer["name"],
                        "dob": designer.get("dob"),
                    },
                }
            )
        return queries

    @staticmethod
    def create_artist_nodes(artists_data):
        """Create Artist nodes"""
        queries = []
        for artist in artists_data:
            query = """
            CREATE (a:Artist {
                id: $id,
                name: $name,
                dob: $dob,
                migrated_at: datetime()
            })
            """
            queries.append(
                {
                    "query": query,
                    "params": {
                        "id": artist["id"],
                        "name": artist["name"],
                        "dob": artist.get("dob"),
                    },
                }
            )
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
                migrated_at: datetime()
            })
            """
            queries.append(
                {
                    "query": query,
                    "params": {
                        "id": genre["id"],
                        "title": genre["name"],
                    },
                }
            )
        return queries

    @staticmethod
    def create_language_nodes(languages_data):
        """Create Language nodes"""
        queries = []
        for lang in languages_data:
            query = """
            CREATE (l:Language {
                id: $id,
                language: $language,
                migrated_at: datetime()
            })
            """
            queries.append({
                'query': query,
                'params': {
                    'id': lang['id'],
                    'language': lang['language']
                }
            })
        return queries

    @staticmethod
    def create_game_relationships(
        game_designers,
        game_artists,
        game_genres,
        game_publishers,
        game_mechanics,
    ):
        """Create relationships between games and
        designers/artists/genres/publishers/mechanics"""
        queries = []

        for gd in game_designers:
            query = """
            MATCH (g:Game {id: $game_id}), (d:Designer {id: $designer_id})
            CREATE (g)-[:DESIGNED_BY]->(d)
            """
            queries.append(
                {
                    "query": query,
                    "params": {
                        "game_id": gd["game_id"],
                        "designer_id": gd["designer_id"],
                    },
                }
            )

        for ga in game_artists:
            query = """
            MATCH (g:Game {id: $game_id}), (a:Artist {id: $artist_id})
            CREATE (g)-[:ART_BY]->(a)
            """
            queries.append(
                {
                    "query": query,
                    "params": {
                        "game_id": ga["game_id"],
                        "artist_id": ga["artist_id"],
                    },
                }
            )

        for gg in game_genres:
            query = """
            MATCH (g:Game {id: $game_id}), (gen:Genre {id: $genre_id})
            CREATE (g)-[:IN_GENRE]->(gen)
            """
            queries.append(
                {
                    "query": query,
                    "params": {
                        "game_id": gg["game_id"],
                        "genre_id": gg["genre_id"],
                    },
                }
            )

        for gp in game_publishers:
            query = """
            MATCH (g:Game {id: $game_id}), (p:Publisher {id: $publisher_id})
            CREATE (g)-[:PUBLISHED_BY]->(p)
            """
            queries.append(
                {
                    "query": query,
                    "params": {
                        "game_id": gp["game_id"],
                        "publisher_id": gp["publisher_id"],
                    },
                }
            )

        for gm in game_mechanics:
            query = """
            MATCH (g:Game {id: $game_id}), (m:Mechanic {id: $mechanic_id})
            CREATE (g)-[:USES_MECHANIC]->(m)
            """
            queries.append(
                {
                    "query": query,
                    "params": {
                        "game_id": gm["game_id"],
                        "mechanic_id": gm["mechanic_id"],
                    },
                }
            )

        return queries

    @staticmethod
    def _create_player_relationships(matchup, players_data):
        """Create relationships between matchups and players"""
        queries = []

        queries.append(
            {
                "query": """
            MATCH (m:Matchup {id: $matchup_id}), (u:User {id: $user_id})
            CREATE (u)-[:PARTICIPATED_IN {role: 'PLAYER1'}]->(m)
            """,
                "params": {
                    "matchup_id": matchup["id"],
                    "user_id": matchup["user_id_1"],
                },
            }
        )

        queries.append(
            {
                "query": """
            MATCH (m:Matchup {id: $matchup_id}), (u:User {id: $user_id})
            CREATE (u)-[:PARTICIPATED_IN {role: 'PLAYER2'}]->(m)
            """,
                "params": {
                    "matchup_id": matchup["id"],
                    "user_id": matchup["user_id_2"],
                },
            }
        )

        if matchup["user_id_winner"] and matchup["user_id_winner"] != 0:
            queries.append(
                {
                    "query": """
                MATCH (m:Matchup {id: $matchup_id}), (u:User {id: $user_id})
                CREATE (u)-[:WON]->(m)
                """,
                    "params": {
                        "matchup_id": matchup["id"],
                        "user_id": matchup["user_id_winner"],
                    },
                }
            )

        if matchup["created_by_user_id"]:
            queries.append(
                {
                    "query": """
                MATCH (m:Matchup {id: $matchup_id}), (u:User {id: $user_id})
                CREATE (u)-[:CREATED]->(m)
                """,
                    "params": {
                        "matchup_id": matchup["id"],
                        "user_id": matchup["created_by_user_id"],
                    },
                }
            )

        return queries

    @staticmethod
    def create_review_nodes_and_relationships(reviews_data):
        """Create Review nodes and relationships - now with direct game_id"""
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
            queries.append(
                {
                    "query": review_query,
                    "params": {
                        "id": review["id"],
                        "title": review["title"],
                        "text": review.get("text", ""),
                        "star_amount": review["star_amount"],
                    },
                }
            )

            queries.append(
                {
                    "query": """
                MATCH (r:Review {id: $review_id}), (u:User {id: $user_id})
                CREATE (u)-[:WROTE]->(r)
                """,
                    "params": {
                        "review_id": review["id"],
                        "user_id": review["user_id"],
                    },
                }
            )

            queries.append(
                {
                    "query": """
                MATCH (r:Review {id: $review_id}), (g:Game {id: $game_id})
                CREATE (r)-[:FOR_GAME]->(g)
                """,
                    "params": {
                        "review_id": review["id"],
                        "game_id": review["game_id"],
                    },
                }
            )

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
            queries.append(
                {
                    "query": query,
                    "params": {
                        "game_id": gr["game_id"],
                        "review_id": gr["review_id"],
                    },
                }
            )
        return queries

    @staticmethod
    def create_video_nodes(videos_data):
        """Create Video nodes"""
        queries = []
        for video in videos_data:
            query = """
            CREATE (v:Video {
                id: $id,
                title: $title,
                category: $category,
                link: $link,
                language: $language,
                migrated_at: datetime()
            })
            """
            queries.append(
                {
                    "query": query,
                    "params": {
                        "id": video["id"],
                        "title": video["title"],
                        "category": video.get("category"),
                        "link": video["link"],
                        "language": video.get("language"),
                    },
                }
            )
        return queries

    @staticmethod
    def create_game_video_relationships(game_videos_data):
        """Create relationships between games and videos"""
        queries = []
        for gv in game_videos_data:
            query = """
            MATCH (g:Game {id: $game_id}), (v:Video {id: $video_id})
            CREATE (g)-[:HAS_VIDEO]->(v)
            """
            queries.append(
                {
                    "query": query,
                    "params": {
                        "game_id": gv["game_id"],
                        "video_id": gv["video_id"],
                    },
                }
            )
        return queries

    @staticmethod
    def create_game_video_relationships(game_videos):
        """Create relationships between games and videos"""
        queries = []
        for game_id, video_ids in game_videos.items():
            for video_id in video_ids:
                query = """
                MATCH (g:Game {id: $game_id}), (v:Video {id: $video_id})
                CREATE (g)-[:HAS_VIDEO]->(v)
                """
                queries.append({
                    'query': query,
                    'params': {
                        'game_id': game_id,
                        'video_id': video_id
                    }
                })
        return queries

    @staticmethod
    def create_video_language_relationships(videos_data):
        """Create relationships between videos and languages"""
        queries = []
        for video in videos_data:
            if video.get('language_id'):
                query = """
                MATCH (v:Video {id: $video_id}), (l:Language {id: $language_id})
                CREATE (v)-[:IN_LANGUAGE]->(l)
                """
                queries.append({
                    'query': query,
                    'params': {
                        'video_id': video['id'],
                        'language_id': video['language_id']
                    }
                })
        return queries