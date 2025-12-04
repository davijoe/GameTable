from typing import Any, List
from pathlib import Path

import xml.etree.ElementTree as ET
import csv
import httpx
import time

from app.settings import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATH = BASE_DIR / "secrets" / "games.csv"


def load_game_ids(limit: int = 20) -> List[str]:
    ids: List[int] = []

    with CSV_PATH.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ids.append(row["id"])
            if len(ids) >= limit:
                break

    print("Returning som idssssssss")
    return ids


def fetch_games_xml(ids: List[int], retries: int = 3, delay: int = 5) -> str:
    joined = ",".join(str(i) for i in ids)
    url = f"{settings.base_url}/thing?id={joined}&ratingcomments=1&videos=1"

    headers = {"Authorization": f"Bearer {settings.api_token}"}

    for attempt in range(1, retries + 1):
        try:
            with httpx.Client() as client:
                print("FØR TIMEOUT")
                resp = client.get(url, headers=headers, timeout=30)
                resp.raise_for_status()
                return resp.text
        except httpx.HTTPStatusError as error:
            status = error.response.status_code
            print(f"Request failed with status {status} on attempt {attempt}/{retries}")
            if 500 <= status < 600 and attempt < retries:
                time.sleep(delay)
                continue
            raise
        except httpx.RequestError as error:
            print(f"Network error on attempt {attempt}/{retries}: {error}")
            if attempt < retries:
                time.sleep(delay)
                continue
            raise


def _parse_game_item(item: ET.Element) -> dict[str, Any]:
    game_id = int(item.attrib["id"])

    thumbnail = item.findtext("thumbnail")
    image = item.findtext("image")
    description = item.findtext("description")

    name_primary = None
    for name_elem in item.findall("name"):
        if name_elem.attrib.get("type") == "primary":
            name_primary = name_elem.attrib.get("value")
            break

    def int_attr(elem_name: str, attr: str = "value") -> int | None:
        elem = item.find(elem_name)
        if elem is not None:
            raw = elem.attrib.get(attr)
            if raw is None:
                return None
            try:
                return int(raw)
            except (TypeError, ValueError):
                return None
        return None

    year_published = int_attr("yearpublished")
    min_players = int_attr("minplayers")
    max_players = int_attr("maxplayers")
    playing_time = int_attr("playingtime")
    min_age = int_attr("minage")

    artists: list[tuple[int, str]] = []
    designers: list[tuple[int, str]] = []
    mechanics: list[tuple[int, str]] = []
    genres: list[tuple[int, str]] = []
    publishers: list[tuple[int, str]] = []
    reviews: list[dict[str, Any]] = []
    videos: list[dict[str, Any]] = []

    for link in item.findall("link"):
        link_type = link.attrib.get("type")
        link_id_raw = link.attrib.get("id")
        value = link.attrib.get("value")
        if not link_id_raw or not value:
            continue
        try:
            link_id = int(link_id_raw)
        except ValueError:
            continue

        if link_type == "boardgameartist":
            artists.append((link_id, value))
        elif link_type == "boardgamedesigner":
            designers.append((link_id, value))
        elif link_type == "boardgamemechanic":
            mechanics.append((link_id, value))
        elif link_type == "boardgamecategory":
            genres.append((link_id, value))
        elif link_type == "boardgamepublisher":
            publishers.append((link_id, value))

    videos_elem = item.find("videos")
    if videos_elem is not None:
        for v in videos_elem.findall("video"):
            video_id_raw = v.attrib.get("id")
            title = v.attrib.get("title")
            category = v.attrib.get("category")
            link = v.attrib.get("link")
            language_name = v.attrib.get("language")

            if not video_id_raw or not title:
                continue

            try:
                video_id = int(video_id_raw)
            except (TypeError, ValueError):
                continue

            videos.append(
                {
                    "id": video_id,
                    "title": title,
                    "category": category or "Unknown",
                    "link": link or "",
                    "language": language_name or "Unknown",
                }
            )

    comments_elem = item.find("comments")
    if comments_elem is not None:
        for c in comments_elem.findall("comment"):
            username = c.attrib.get("username")
            rating_raw = c.attrib.get("rating")
            text = c.attrib.get("value")

            if not username or not text:
                continue

            if rating_raw is None or rating_raw == "N/A":
                rating_val: int | None = None
            else:
                try:
                    rating_val = int(rating_raw)
                except ValueError:
                    rating_val = None

            reviews.append(
                {
                    "username": username,
                    "text": text,
                    "rating": rating_val,
                }
            )

    return {
        "id": game_id,
        "name": name_primary or "",
        "description": description,
        "image": image,
        "videos": videos,
        "thumbnail": thumbnail,
        "year_published": year_published,
        "min_players": min_players,
        "max_players": max_players,
        "playing_time": playing_time,
        "minimum_age": min_age,
        "artists": artists,
        "designers": designers,
        "mechanics": mechanics,
        "genres": genres,
        "publishers": publishers,
        "reviews": reviews,
    }


def parse_game_xml(xml_text: str) -> dict[str, Any]:
    # single item version - useful for debugging
    root = ET.fromstring(xml_text)
    item = root.find("item")
    if item is None:
        raise ValueError("No <item> element found in BGG response")
    return _parse_game_item(item)


def parse_games_xml(xml_text: str) -> list[dict[str, Any]]:
    # multi item version for batched calls
    root = ET.fromstring(xml_text)
    games: list[dict[str, Any]] = []

    for item in root.findall("item"):
        try:
            games.append(_parse_game_item(item))
        except Exception as exc:
            print(f"Failed to parse item {item.attrib.get('id')}: {exc}")
            continue

    return games
