from fastapi import FastAPI
from app.controller.game_controller import router as game_router
from app.controller.matchup_controller import router as matchup_router

app = FastAPI(title="Game API")

app.include_router(game_router)
app.include_router(matchup_router)

# Optional health endpoint


@app.get("/healthz")
def health():
    return {"status": "ok"}
