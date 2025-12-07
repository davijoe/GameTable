import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controller.artist_controller import router as artist_router
from app.controller.auth_controller import router as auth_router
from app.controller.designer_controller import router as designer_router
from app.controller.game_controller import router as game_router
from app.controller.genre_controller import router as genre_router
from app.controller.user_controller import router as user_router
from app.controller.weather_controller import router as weather_router

app = FastAPI(title="Game API")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(artist_router)
app.include_router(designer_router)
app.include_router(game_router)
app.include_router(genre_router)
app.include_router(user_router)
app.include_router(weather_router)


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/db")
def db_info():
    return {"active_database": os.getenv("DB_MODE")}
