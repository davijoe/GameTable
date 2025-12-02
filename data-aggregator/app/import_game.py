from app.utility.mysql import SessionLocal
from app.service.import_game_to_mysql import (
    upsert_game_from_parsed,
    fetch_game_xml,
    parse_game_xml,
)


def run_import(game_id: int):
    xml_text = fetch_game_xml(game_id)
    data = parse_game_xml(xml_text)

    with SessionLocal() as db:
        game = upsert_game_from_parsed(db, data)
        print(f"Imported game: {game_id} : {game.name}")


if __name__ == "__main__":
    run_import(1)
