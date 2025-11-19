from fastapi import FastAPI

from app.service.games_service import fetch_games_xml, load_game_ids, parse_games_xml

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


if __name__ == "__main__":
    main()
