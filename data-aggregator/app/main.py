from fastapi import FastAPI

from pymongo import MongoClient

from app.service.games_service import fetch_games_xml, load_game_ids, parse_games_xml
from app.settings import settings

app = FastAPI()


MONGO_USER = settings.mongo_root_username
MONGO_PASS = settings.mongo_root_password


def get_mongo_collection():
    uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@localhost:27017/gametable?authSource=admin"
    client = MongoClient(uri)
    db = client["gametable"]
    return db["bgg_games"]


def save_games_to_mongo(games, collection):
    inserted_ids = []

    for game in games:
        # Use BGG ID as the Mongo _id so you do not insert duplicates
        game_id = int(game["id"])

        doc = {
            "_id": game_id,  # unique key in Mongo
            "bgg_id": game_id,
            "name": game["name"],
            "thumbnail": game["thumbnail"],
            "image": game["image"],
            "year_published": game["year_published"],
            "min_players": game["min_players"],
            "max_players": game["max_players"],
            "designers": game["game_designer"],
            "artists": game["artists"],
            "categories": game["categories"],
        }

        # Upsert so running the scraper twice will update instead of duplicating
        result = collection.update_one(
            {"_id": game_id},
            {"$set": doc},
            upsert=True,
        )

        if result.upserted_id is not None:
            inserted_ids.append(result.upserted_id)

    return inserted_ids


def main():
    ids = load_game_ids(limit=1)
    xml_text = fetch_games_xml(ids)
    games = parse_games_xml(xml_text)

    collection = get_mongo_collection()
    inserted_ids = save_games_to_mongo(games, collection)

    print("Inserted IDs:", inserted_ids)


def main2():
    print("Hello from bgg-scraper!")

    # Load up to 20 IDs from secrets/games.csv
    ids = load_game_ids(limit=1)
    print("Loaded IDs:", ids)

    # Fetch XML
    xml_text = fetch_games_xml(ids)

    # Parse and Print
    games = parse_games_xml(xml_text)

    for game in games:
        print("ID:", game["id"])
        print("Name:", game["name"])
        print("Thumbnail:", game["thumbnail"])
        print("Image:", game["image"])
        print("Description:", (game["description"] or "")[:200], "...")
        print("Year published:", game["year_published"])
        print("Min players:", game["min_players"])
        print("Max players:", game["max_players"])
        print("Designers:", game["game_designer"])
        print("Artists:", game["artists"])
        print("Categories:", game["categories"])
        print("-" * 40)


if __name__ == "__main__":
    main()
