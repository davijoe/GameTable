from fastapi import FastAPI

from pymongo import MongoClient

from app.service.games_service import fetch_games_xml, load_game_ids, parse_games_xml
from app.settings import settings

app = FastAPI()


def main():
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


MONGO_USER = settings.mongo_root_username
MONGO_PASS = settings.mongo_root_password


def notmain():
    uri = f"mongodb://{MONGO_USER}:{MONGO_PASS}@localhost:27017/gametable?authSource=admin"

    doc = {
        "name": "Example",
        "value": 123,
        "items": ["a", "b", "c"],
    }

    client = MongoClient(uri)
    db = client["gametable"]
    collection = db["test_collection"]
    inserted = collection.insert_one(doc)
    print("Inserted ID:", inserted.inserted_id)


if __name__ == "__main__":
    # main()
    notmain()
