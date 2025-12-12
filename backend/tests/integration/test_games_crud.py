def test_create_get_update_delete_game(client):
    payload = {
        "name": "Chess",
        "description": "Is playable. Mucho fun oui oui",
    }

    r = client.post("/api/games", json=payload)
    assert r.status_code == 201, r.text
    created = r.json()
    assert created["name"] == "Chess"
