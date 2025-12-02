import xml.etree.ElementTree as ET
from typing import Any

import requests
from app.models.artist_model import Artist
from app.models.designer_model import Designer
from app.models.game_model import Game
from app.models.genre_model import Genre
from app.models.mechanic_model import Mechanic
from sqlalchemy.orm import Session

BGG_THING_URL = "https://boardgamegeek.com/xmlapi2/thing?id={game_id}&stats=0"


def fetch_game_xml(game_id: int) -> str:
    url = BGG_THING_URL.format(game_id=game_id)
    resp = requests.get(url, timeout=30)
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

    return {
        "id": game_id,
        "name": name_primary or "",
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
    }


def upsert_game_from_parsed(db: Session, data: dict[str, Any]) -> Game:
    game_id = data["id"]

    game = db.get(Game, game_id)
    if game is None:
        game = Game(id=game_id)

    game.name = data["name"]
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

    db.add(game)
    db.commit()
    db.refresh(game)

    return game
