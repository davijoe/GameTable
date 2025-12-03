from app.utility.mysql import SessionLocal
from app.service.import_game_to_mysql import (
    upsert_game_from_parsed,
    fetch_game_xml,
    parse_game_xml,
)

import time

from app.service.games_service import load_game_ids


def import_games_from_csv(limit: int = 20) -> None:
    id_strings: list[str] = load_game_ids(limit=limit)
    game_ids = [int(x) for x in id_strings]

    total = len(game_ids)
    print(f"Importing {len(game_ids)} games from CSV: {game_ids}")

    with SessionLocal() as db:
        for index, game_id in enumerate(game_ids, start=1):
            import_start = time.time()

            try:
                xml_text = fetch_game_xml(game_id)
                data = parse_game_xml(xml_text)
                game = upsert_game_from_parsed(db, data)
                print(f"Imported game: {game_id} : {game.name}")

            except Exception as exc:
                print(f"Failed to import game {game_id}: {exc}")

            import_end = time.time()
            elapsed_time = import_start - import_end
            avg_per_game = elapsed_time / index
            remaining = (total - index) * avg_per_game

            print(
                f"[{index}/{total}] \n"
                f"  This game: {elapsed_time:.2f}s\n"
                f"  Total elapsed: {elapsed_time:.2f}s\n"
                f"  ETA remaining: {remaining:.2f}s\n"
            )


def run_import(game_id: int):
    with SessionLocal() as db:
        xml_text = fetch_game_xml(game_id)
        data = parse_game_xml(xml_text)
        game = upsert_game_from_parsed(db, data)
        print(f"Imported game: {game_id} : {game.name}")


if __name__ == "__main__":
    # run_import(1)
    import_games_from_csv(limit=20)
