import uuid

"""
POSITIVE TESTS
- test creating a game
- test getting a game
- test getting game detail
- test listing games
- test listing games with pagination
- test listing games with search q
"""


def create_game(client, *, name="Chess", description="Fun", bgg_rating=5.5):
    r = client.post(
        "/api/games",
        json={
            "name": name,
            "description": description,
            "bgg_rating": bgg_rating,
        },
    )
    assert r.status_code == 201, r.text
    data = r.json()
    assert "id" in data
    return data


def test_create_game_returns_201_and_body(client, _allow_admin):
    created = create_game(
        client,
        name="Chess",
        description="Mucho fun",
        bgg_rating=8.0,
    )

    assert created["name"] == "Chess"
    assert created["description"] == "Mucho fun"
    assert created["bgg_rating"] == 8.0
    assert isinstance(created["id"], int)
    assert created["id"] > 0


def test_get_game_gives_200(client, _allow_admin):
    created = create_game(
        client,
        name="Checkers",
        description="A fun board game",
        bgg_rating=7.2,
    )
    game_id = created["id"]

    r = client.get(f"/api/games/{game_id}")
    assert r.status_code == 200, r.text
    fetched = r.json()

    assert fetched["id"] == game_id
    assert fetched["name"] == "Checkers"
    assert fetched["description"] == "A fun board game"
    assert fetched["bgg_rating"] == 7.2


def test_get_game_detail_gives_200(client, _allow_admin):
    created = create_game(client, name="Catan", description="Trade", bgg_rating=7.8)
    game_id = created["id"]

    r = client.get(f"/api/games/{game_id}/detail")
    assert r.status_code == 200, r.text
    detail = r.json()

    assert detail["id"] == game_id
    assert detail["name"] == "Catan"


def test_list_games_has_expected_shape(client, _allow_admin):
    create_game(client, name=f"A-{uuid.uuid4()}", description="d", bgg_rating=1.0)
    create_game(client, name=f"B-{uuid.uuid4()}", description="d", bgg_rating=2.0)

    r = client.get("/api/games")
    assert r.status_code == 200, r.text
    data = r.json()

    assert set(data.keys()) == {"total", "offset", "limit", "items"}
    assert isinstance(data["total"], int)
    assert isinstance(data["offset"], int)
    assert isinstance(data["limit"], int)
    assert isinstance(data["items"], list)


def test_list_games_pagination_offset_limit(client, _allow_admin):
    create_game(client, name=f"P1-{uuid.uuid4()}", description="d", bgg_rating=1.0)
    create_game(client, name=f"P2-{uuid.uuid4()}", description="d", bgg_rating=2.0)
    create_game(client, name=f"P3-{uuid.uuid4()}", description="d", bgg_rating=3.0)

    r = client.get("/api/games?offset=0&limit=2")
    assert r.status_code == 200, r.text
    page1 = r.json()
    assert page1["offset"] == 0
    assert page1["limit"] == 2
    assert len(page1["items"]) <= 2
    assert page1["total"] >= 3

    r = client.get("/api/games?offset=2&limit=2")
    assert r.status_code == 200, r.text
    page2 = r.json()
    assert page2["offset"] == 2
    assert page2["limit"] == 2


def test_list_games_search_q_filters(client, _allow_admin):
    needle = f"Needle-{uuid.uuid4()}"
    create_game(client, name=needle, description="hello", bgg_rating=5.0)
    create_game(
        client, name=f"Other-{uuid.uuid4()}", description="world", bgg_rating=5.0
    )

    r = client.get(f"/api/games?q={needle}")
    assert r.status_code == 200, r.text
    data = r.json()

    names = [x.get("name") for x in data["items"]]
    assert any(n == needle for n in names)


def test_update_game_patch_changes_fields(client, _allow_admin):
    created = create_game(client, name="Monopoly", description="Old", bgg_rating=6.5)
    game_id = created["id"]

    r = client.patch(
        f"/api/games/{game_id}",
        json={"description": "New", "bgg_rating": 7.0},
    )
    assert r.status_code == 200, r.text
    updated = r.json()

    assert updated["id"] == game_id
    assert updated["name"] == "Monopoly"
    assert updated["description"] == "New"
    assert updated["bgg_rating"] == 7.0


def test_delete_game_then_get_404(client, _allow_admin):
    created = create_game(client, name="Risk", description="War", bgg_rating=6.0)
    game_id = created["id"]

    r = client.delete(f"/api/games/{game_id}")
    assert r.status_code == 204, r.text

    r = client.get(f"/api/games/{game_id}")
    assert r.status_code == 404


def test_get_unknown_game_returns_404(client, _allow_admin):
    r = client.get("/api/games/999999999")
    assert r.status_code == 404


def test_update_unknown_game_returns_404(client, _allow_admin):
    r = client.patch("/api/games/999999999", json={"description": "x"})
    assert r.status_code == 404


def test_delete_unknown_game_returns_404(client, _allow_admin):
    r = client.delete("/api/games/999999999")
    assert r.status_code == 404


def test_create_game_missing_fields_returns_422(client, _allow_admin):
    r = client.post("/api/games", json={"description": "x"})
    assert r.status_code == 422


def test_create_game_wrong_types_returns_422(client, _allow_admin):
    r = client.post(
        "/api/games",
        json={"name": 123, "description": ["nope"], "bgg_rating": "high"},
    )
    assert r.status_code == 422


def test_create_game_requires_admin_returns_403(client, _deny_admin):
    r = client.post(
        "/api/games",
        json={"name": "Nope", "description": "x", "bgg_rating": 5.0},
    )
    assert r.status_code == 403


# def test_list_games_negative_limit_returns_422(client, _allow_admin):
#    r = client.get("/api/games?limit=-1")
#    assert r.status_code == 404, r.text
