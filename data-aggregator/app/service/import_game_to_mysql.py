import xml.etree.ElementTree as ET
from typing import Any

import os
import requests

from app.model.artist_model import Artist
from app.model.designer_model import Designer
from app.model.game_model import Game
from app.model.genre_model import Genre
from app.model.mechanic_model import Mechanic
from app.model.publisher_model import Publisher
from app.model.review_model import Review
from app.service.user_service import get_or_create_bgg_user

from app.settings import settings

from sqlalchemy.orm import Session

API_KEY = os.getenv("API_KEY")


def fetch_game_xml(game_id: int) -> str:
    url = f"{settings.base_url}/thing?id={game_id}&ratingcomments=1&videos=1"

    headers = {"Authorization": f"Bearer {settings.api_token}"}

    print(f"Calling {url} with headers: {headers}...")

    resp = requests.get(url, headers=headers, timeout=30)

    print("Status:", resp.status_code)
    print("Body (first 300 chars):", resp.text[:300])

    resp.raise_for_status()
    return resp.text


def parse_game_xml(xml_text: str) -> dict[str, Any]:
    root = ET.fromstring(xml_text)

    item = root.find("item")
    if item is None:
        raise ValueError("No <item> element found in BGG response")

    game_id = int(item.attrib["id"])

    # thumbnail and image
    thumbnail = item.findtext("thumbnail")
    image = item.findtext("image")

    # description
    description = item.findtext("description")

    # primary name
    name_primary = None
    for name_elem in item.findall("name"):
        if name_elem.attrib.get("type") == "primary":
            name_primary = name_elem.attrib.get("value")
            break

    # numeric fields
    def int_attr(elem_name: str, attr: str = "value") -> int | None:
        elem = item.find(elem_name)
        if elem is not None:
            try:
                return int(elem.attrib.get(attr))
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

    # BGG "comments" -> our "reviews"
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


def upsert_game_from_parsed(db: Session, data: dict[str, Any]) -> Game:
    game_id = data["id"]

    game = db.get(Game, game_id)
    if game is None:
        game = Game(id=game_id)

    game.name = data["name"]
    game.description = data["description"]
    game.image = data["image"]
    game.thumbnail = data["thumbnail"]
    game.year_published = data["year_published"]
    game.min_players = data["min_players"]
    game.max_players = data["max_players"]
    game.playing_time = data["playing_time"]
    game.minimum_age = data["minimum_age"]

    # clear existing relations to avoid duplicates
    game.artists.clear()
    game.designers.clear()
    game.mechanics.clear()
    game.genres.clear()
    game.publishers.clear()

    for existing_review in list(game.reviews):
        db.delete(existing_review)
    game.reviews.clear()

    # artists
    for artist_id, artist_name in data["artists"]:
        artist = db.get(Artist, artist_id)
        if artist is None:
            artist = Artist(id=artist_id, name=artist_name)
        else:
            if not artist.name:
                artist.name = artist_name
        game.artists.append(artist)

    # designers
    for designer_id, designer_name in data["designers"]:
        designer = db.get(Designer, designer_id)
        if designer is None:
            designer = Designer(id=designer_id, name=designer_name)
        else:
            if not designer.name:
                designer.name = designer_name
        game.designers.append(designer)

    # mechanics
    for mechanic_id, mechanic_name in data["mechanics"]:
        mechanic = db.get(Mechanic, mechanic_id)
        if mechanic is None:
            mechanic = Mechanic(id=mechanic_id, name=mechanic_name)
        else:
            if not mechanic.name:
                mechanic.name = mechanic_name
        game.mechanics.append(mechanic)

    # genres
    for genre_id, genre_name in data["genres"]:
        genre = db.get(Genre, genre_id)
        if genre is None:
            genre = Genre(id=genre_id, name=genre_name)
        else:
            if not genre.name:
                genre.name = genre_name
        game.genres.append(genre)

    # publishers
    for publisher_id, publisher_name in data["publishers"]:
        publisher = db.get(Publisher, publisher_id)
        if publisher is None:
            publisher = Publisher(id=publisher_id, name=publisher_name)
        else:
            if not publisher.name:
                publisher.name = publisher_name
        game.publishers.append(publisher)

    # reviews (from XMLAPI2 "comments")
    for r in data.get("reviews", []):
        username = r["username"]
        text = r["text"]
        rating_val = r["rating"]

        user = get_or_create_bgg_user(db, username)

        if rating_val is None:
            star_amount = 0
        else:
            star_amount = int(round(rating_val))

        title = text[:70] or username
        review = Review(
            title=title,
            text=text[:255],
            star_amount=star_amount,
            user=user,
        )

        game.reviews.append(review)
        db.add(review)

    db.add(game)
    db.commit()
    db.refresh(game)

    return game
