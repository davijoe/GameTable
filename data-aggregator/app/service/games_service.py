from pathlib import Path
import csv
from typing import List
import httpx
import xml.etree.ElementTree as ET

from app.settings import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATH = BASE_DIR / "secrets" / "games.csv"


def load_game_ids(limit: int = 20) -> List[str]:
    ids: List[str] = []

    with CSV_PATH.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ids.append(row["id"])
            if len(ids) >= limit:
                break

    return ids


def fetch_games_xml(ids: List[str]) -> str:
    joined = ",".join(ids)
    url = f"{settings.base_url}/thing?id={joined}"

    headers = {"Authorization": f"Bearer {settings.api_token}"}

    with httpx.Client() as client:
        r = client.get(url, headers=headers)
        r.raise_for_status()
        return r.text


def parse_games_xml(xml_text: str):
    root = ET.fromstring(xml_text)
    results = []

    for item in root.findall("item"):
        game_id = item.get("id")

        thumbnail = None
        tn = item.find("thumbnail")
        if tn is not None:
            thumbnail = tn.text

        image = None
        img = item.find("image")
        if img is not None:
            image = img.text

        name_primary = None
        for name in item.findall("name"):
            if name.get("type") == "primary":
                name_primary = name.get("value")

        description = None
        desc = item.find("description")
        if desc is not None:
            description = desc.text

        year_published = None
        yp = item.find("yearpublished")
        if yp is not None:
            year_published = yp.get("value")

        min_players = None
        minp = item.find("minplayers")
        if minp is not None:
            min_players = minp.get("value")

        max_players = None
        maxp = item.find("maxplayers")
        if maxp is not None:
            max_players = maxp.get("value")

        playing_time = None
        pt = item.find("playingtime")
        if pt is not None:
            playing_time = pt.get("value")

        min_age = None
        ma = item.find("minage")
        if ma is not None:
            min_age = ma.get("value")

        links = item.findall("link")

        designers = []
        for link in links:
            if link.get("type") == "boardgamedesigner":
                value = link.get("value")
                if value is not None:
                    designers.append(value)

        artists = []
        for link in links:
            if link.get("type") == "boardgameartist":
                value = link.get("value")
                if value is not None:
                    artists.append(value)

        categories = []
        for link in links:
            if link.get("type") == "boardgamecategory":
                value = link.get("value")
                if value is not None:
                    categories.append(value)

        results.append(
            {
                "id": game_id,
                "thumbnail": thumbnail,
                "image": image,
                "name": name_primary,
                "description": description,
                "year_published": year_published,
                "min_players": min_players,
                "max_players": max_players,
                "playing_time": playing_time,
                "minimum_age": min_age,
                "game_designer": designers,
                "artists": artists,
                "categories": categories,
            }
        )

    return results
