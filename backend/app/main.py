from fastapi import FastAPI
from app.controller.game_controller import router as game_router

app = FastAPI(title="Game API")

app.include_router(game_router)

# Optional health endpoint


@app.get("/healthz")
def health():
    return {"status": "ok"}
