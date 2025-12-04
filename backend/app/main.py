from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controller.artist_controller import router as artist_router
from app.controller.designer_controller import router as designer_router
from app.controller.game_controller import router as game_router
from app.controller.genre_controller import router as genre_router
from app.controller.user_controller import router as user_router
import os
app = FastAPI(title="Game API")

origins = [
    "http://localhost:5173",  #harcoded to what vite uses standard when run with "bun run dev"
    "http://localhost:3000" # works with docker
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(designer_router)
app.include_router(game_router)
app.include_router(user_router)
app.include_router(genre_router)
app.include_router(artist_router)


@app.get("/healthz")
def health():
    return {"status": "ok"}

@app.get("/db")
def db_info():
    return {"active_database": os.getenv("DB_MODE", "sql")}