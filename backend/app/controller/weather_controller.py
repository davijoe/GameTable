
from typing import Any

import requests
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/weather", tags=["weather"])

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"




@router.get("/geo", response_model=dict[str, Any])
def get_weather_geo(
    latitude: float = Query(...),
    longitude: float = Query(...),
):
    return fetch_weather(latitude, longitude)


def fetch_weather(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
    }
    try:
        r = requests.get(OPEN_METEO_URL, params=params, timeout=5)
    except requests.RequestException as exc:
        raise HTTPException(502, f"Failed to contact weather provider (open-meteo): {exc}")

    if r.status_code != 200:
        raise HTTPException(502, "Weather provider (open-meteo) returned an error")
    return r.json()

