from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controller.artist_controller import router as artist_router
from app.controller.designer_controller import router as designer_router
from app.controller.game_controller import router as game_router
from app.controller.genre_controller import router as genre_router
from app.controller.matchup_controller import router as matchup_router
from app.controller.move_controller import router as move_router
from app.controller.user_controller import router as user_router

app = FastAPI(title="Game API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(designer_router)
app.include_router(game_router)
app.include_router(matchup_router)
app.include_router(user_router)
app.include_router(genre_router)
app.include_router(artist_router)
app.include_router(move_router)


@app.get("/healthz")
def health():
    return {"status": "ok"}
