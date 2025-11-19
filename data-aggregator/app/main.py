from fastapi import FastAPI
import time

from app.service.games_service import fetch_games_xml, load_game_ids, parse_games_xml
from app.utility.db import get_mongo_collection
from app.service.mongo_service import save_games_to_mongo

app = FastAPI()


def newmain():
    all_ids = load_game_ids(170669)
    batch_size = 20
    collection = get_mongo_collection()

    total_new_games = 0

    for start in range(0, len(all_ids), batch_size):
        batch = all_ids[start : start + batch_size]

        print("Processing IDs:", batch)

        xml_text = fetch_games_xml(batch)
        games = parse_games_xml(xml_text)

        # Do some stuff with the parsed games
        inserted_ids = save_games_to_mongo(games, collection)
        total_new_games += len(inserted_ids)

        print(f"Total new games added: {total_new_games}")

        if start + batch_size < len(all_ids):
            time.sleep(5)


if __name__ == "__main__":
    newmain()
