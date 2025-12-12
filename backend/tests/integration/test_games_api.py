def make_valid_game_payload(**overrides):
    base = {
        "name": "Catan",
        "slug": "catan",
        "year_published": 1995,
        "bgg_rating": 7.2,
        "difficulty_rating": 2.3,
        "description": "A classic resource management game.",
        "min_players": 3,
        "max_players": 4,
        "thumbnail": "https://example.com/thumb.jpg",
        "image": "https://example.com/image.jpg",
    }
    base.update(overrides)
    return base


def test_create_game_success(client):
    payload = make_valid_game_payload()

    response = client.post("/games", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == payload["name"]
    assert data["slug"] == payload["slug"]
    assert "id" in data
