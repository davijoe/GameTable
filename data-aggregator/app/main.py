import time
from datetime import timedelta

from fastapi import FastAPI

from app.service.games_service import fetch_games_xml, load_game_ids, parse_games_xml
from app.service.mongo_service import save_games_to_mongo
from app.utility.db import get_mongo_collection

app = FastAPI()


def newmain():
    all_ids = load_game_ids(170701)
    batch_size = 20
    collection = get_mongo_collection()

    new_games = 0
    parsed_games = 0

    start_time = time.time()

    for start in range(0, len(all_ids), batch_size):
        batch = all_ids[start : start + batch_size]

        print("Processing IDs:", batch)

        xml_text = fetch_games_xml(batch)
        games = parse_games_xml(xml_text)

        # Do some stuff with the parsed games
        inserted_ids = save_games_to_mongo(games, collection)
        new_games += len(inserted_ids)
        parsed_games += len(batch)

        elapsed_seconds = int(time.time() - start_time)
        elapsed_formatted = str(timedelta(seconds=elapsed_seconds))

        print(f"Added: {new_games} | Parsed: {parsed_games} | {elapsed_formatted}")

        if start + batch_size < len(all_ids):
            time.sleep(5)


if __name__ == "__main__":
    newmain()
