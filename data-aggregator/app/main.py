from fastapi import FastAPI

from app.service.games_service import fetch_games_xml, load_game_ids, parse_games_xml
from app.utility.db import get_mongo_collection
from app.service.mongo_service import save_games_to_mongo

app = FastAPI()


def main():
    ids = load_game_ids(limit=20)
    xml_text = fetch_games_xml(ids)
    games = parse_games_xml(xml_text)

    collection = get_mongo_collection()
    inserted_ids = save_games_to_mongo(games, collection)

    print(f"Newly inserted {len(inserted_ids)} games into MongoDB")


if __name__ == "__main__":
    main()
