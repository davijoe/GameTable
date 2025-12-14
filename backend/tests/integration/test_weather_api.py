"""
Postive Integration Tests
 - Get request with correct parameters that should return status code 200

"""


def testy_testy(client):
    r = client.get("/api/weather/geo?latitude=55.6761&longitude=12.5683")

    assert r.status_code == 200


def test_weather_geo_valid_request_returns_200_and_json(client):
    r = client.get("/api/weather/geo?latitude=55.6761&longitude=12.5683")

    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/json")

    data = r.json()
    assert isinstance(data, dict)


"""
Negative Integration Tests
 - Testing with
    * Missing Parameters
    * Invalid Parameter Types
"""


def test_weather_geo_missing_params_returns_422(client):
    r = client.get("/api/weather/geo?latitude=55.6761")
    assert r.status_code == 422


def test_weather_geo_invalid_types_returns_422(client):
    r = client.get("/api/weather/geo?latitude=not-a-float&longitude=12.5683")
    assert r.status_code == 422


def test_weather_geo_empty_query_returns_422(client):
    r = client.get("/api/weather/geo")
    assert r.status_code == 422
