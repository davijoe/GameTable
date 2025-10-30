from fastapi import FastAPI
from app.controller.game_controller import router as game_router
from app.controller.artist_controller import router as artist_router

app = FastAPI(title="Game API")

app.include_router(game_router)
app.include_router(artist_router)

# Optional health endpoint


@app.get("/healthz")
def health():
    return {"status": "ok"}
