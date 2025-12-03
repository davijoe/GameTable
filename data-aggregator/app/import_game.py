from app.utility.mysql import SessionLocal
from app.service.import_game_to_mysql import (
    upsert_game_from_parsed,
    parse_game_xml,
)
from app.service.games_service import (
    fetch_games_xml,
    load_game_ids,
)
import time


def import_games_from_csv(limit: str = 10) -> None:
    game_ids: list[int] = load_game_ids(limit=limit)

    total = len(game_ids)
    print(f"Importing {len(game_ids)} games from CSV: {game_ids}")

    with SessionLocal() as db:
        import_start = time.time()
        print(f"Initiating API sucking at time:{import_start}")
        for index, game_id in enumerate(game_ids, start=1):
            try:
                print("Trying hard! XML fetch")
                xml_text = fetch_games_xml([game_id])

                print("Trying hard! Parsing!")
                data = parse_game_xml(xml_text)

                print("Trying hard! Upserting!")
                game = upsert_game_from_parsed(db, data)
                print(f"Imported game: {game_id} : {game.name}")

            except Exception as exc:
                print(f"Failed to import game {game_id}: {exc}")

            now = time.time()
            elapsed_time = now - import_start
            avg_per_game = elapsed_time / index

            print(
                f"elapsed_time: {elapsed_time} | Average time per game: {avg_per_game}"
            )
        print(f"total games imported: {total}")


def run_import(game_id: int):
    with SessionLocal() as db:
        xml_text = fetch_games_xml([str(game_id)])
        data = parse_game_xml(xml_text)
        game = upsert_game_from_parsed(db, data)
        print(f"Imported game: {game_id} : {game.name}")


if __name__ == "__main__":
    # run_import(1)
    import_games_from_csv(limit=10)
    # run_import()
