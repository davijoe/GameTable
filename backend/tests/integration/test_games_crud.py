import pytest
import uuid

"""
HAPPY PATH / POSITIVE INTEGRATION TESTS

These tests verify the expected behavior of the Games API when:
- inputs are valid
- resources exist
- the caller has sufficient permissions

They assert that the API:
- returns correct HTTP status codes
- retrieves data correctly
- returns JSON responses with the expected fields, data types, and values


These tests represent normal, supported usage of the API.
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


def test_create_game_returns_201(client, _allow_admin):
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


"""
NEGATIVE AND DEFENSIVE TESTS

These tests ensure the API is resilient against incorrect usage.
They validate error handling, authorization enforcement, and boundary conditions.
The goal is to guarantee that invalid requests do not lead to undefined behavior,
silent failures, or unintended state changes.
"""


def test_delete_game_get_404(client, _allow_admin):
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


def test_get_game_with_non_int_id_returns_404(client, _allow_admin):
    r = client.get("/api/games/not-an-int")
    assert r.status_code == 404


def test_patch_game_with_non_int_id_returns_404(client, _allow_admin):
    r = client.patch("/api/games/not-an-int", json={"description": "x"})
    assert r.status_code == 404


def test_delete_game_with_non_int_id_returns_404(client, _allow_admin):
    r = client.delete("/api/games/not-an-int")
    assert r.status_code == 404


def test_create_game_empty_payload_returns_422(client, _allow_admin):
    r = client.post("/api/games", json={})
    assert r.status_code == 422


def test_create_game_null_fields_raises_error(client, _allow_admin):
    with pytest.raises(AttributeError):
        client.post(
            "/api/games",
            json={"name": None, "description": None, "bgg_rating": None},
        )


def test_create_game_empty_name_returns_422(client, _allow_admin):
    r = client.post(
        "/api/games",
        json={"name": "", "description": "x", "bgg_rating": 5.0},
    )
    assert r.status_code == 422


def test_create_game_negative_rating_returns_422(client, _allow_admin):
    r = client.post(
        "/api/games",
        json={"name": "Bad", "description": "x", "bgg_rating": -1.0},
    )
    assert r.status_code == 422


def test_create_game_too_high_rating_returns_422(client, _allow_admin):
    r = client.post(
        "/api/games",
        json={"name": "Too High", "description": "x", "bgg_rating": 100.0},
    )
    assert r.status_code == 422


def test_patch_game_with_no_fields_is_noop_returns_200(client, _allow_admin):
    created = create_game(client, name="PatchMe", description="x", bgg_rating=5.0)
    game_id = created["id"]

    r = client.patch(f"/api/games/{game_id}", json={})
    assert r.status_code == 200, r.text
    updated = r.json()

    assert updated["id"] == game_id
    assert updated["name"] == "PatchMe"
    assert updated["description"] == "x"
    assert updated["bgg_rating"] == 5.0


def test_patch_game_with_invalid_field_types_returns_422(client, _allow_admin):
    created = create_game(client, name="PatchBad", description="x", bgg_rating=5.0)
    game_id = created["id"]

    r = client.patch(
        f"/api/games/{game_id}",
        json={"description": 123, "bgg_rating": "high"},
    )
    assert r.status_code == 422


def test_patch_game_requires_admin_returns_403(client, _deny_admin):
    r = client.patch("/api/games/1", json={"description": "nope"})
    assert r.status_code == 403


def test_delete_game_requires_admin_returns_403(client, _deny_admin):
    r = client.delete("/api/games/1")
    assert r.status_code == 403


def test_list_games_negative_offset_returns_200(client, _allow_admin):
    r = client.get("/api/games?offset=-1")
    assert r.status_code == 200


def test_list_games_negative_limit_returns_200(client, _allow_admin):
    r = client.get("/api/games?limit=-5")
    assert r.status_code == 200


def test_list_games_zero_limit_returns_200(client, _allow_admin):
    r = client.get("/api/games?limit=0")
    assert r.status_code == 200


def test_list_games_large_offset_returns_200_with_empty_items(client, _allow_admin):
    r = client.get("/api/games?offset=999999&limit=10")
    assert r.status_code == 200
    data = r.json()
    assert data["items"] == []


def test_double_delete_game_returns_404(client, _allow_admin):
    created = create_game(client, name="Temp", description="x", bgg_rating=5.0)
    game_id = created["id"]

    r = client.delete(f"/api/games/{game_id}")
    assert r.status_code == 204

    r = client.delete(f"/api/games/{game_id}")
