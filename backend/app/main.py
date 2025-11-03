from fastapi import FastAPI

from app.controller.artist_controller import router as artist_router
from app.controller.designer_controller import router as designer_router
from app.controller.game_controller import router as game_router
from app.controller.genre_controller import router as genre_router
from app.controller.move_controller import router as move_router

app = FastAPI(title="Game API")

app.include_router(designer_router)
app.include_router(game_router)
app.include_router(genre_router)
app.include_router(artist_router)
app.include_router(move_router)


@app.get("/healthz")
def health():
    return {"status": "ok"}
