def save_games_to_mongo(games, collection):
    inserted_ids = []

    for game in games:
        game_id = int(game["id"])

        doc = {
            "_id": game_id,
            "name": game["name"],
            "thumbnail": game["thumbnail"],
            "image": game["image"],
            "year_published": game["year_published"],
            "min_players": game["min_players"],
            "max_players": game["max_players"],
            "playing_time": game["playing_time"],
            "minimum_age": game["minimum_age"],
            "designers": game["game_designer"],
            "artists": game["artists"],
            "categories": game["categories"],
        }

        # Upsert to avoid duplicates
        result = collection.update_one(
            {"_id": game_id},
            {"$set": doc},
            upsert=True,
        )

        if result.upserted_id is not None:
            inserted_ids.append(result.upserted_id)

    return inserted_ids
