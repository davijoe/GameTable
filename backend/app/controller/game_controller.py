from typing import Any

from fastapi import APIRouter, Depends, HTTPException

# from sqlalchemy.orm import Session
from app.schema.game_schema import GameCreate, GameDetail, GameRead, GameUpdate
from app.service.game_service import GameService
from app.utility.auth import require_admin

router = APIRouter(prefix="/api/games", tags=["games"])


@router.get("", response_model=dict[str, Any])
def list_games(
    q: str | None = None,
    offset: int = 0,
    limit: int = 50,
):
    svc = GameService()
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.get(
    "/{game_id}/detail",
    response_model=GameDetail,
)
def get_game_detail(game_id: str):
    svc = GameService()
    item = svc.get_detail(game_id)
    if not item:
        raise HTTPException(404, "Game not found")
    return item


@router.get("/{game_id}", response_model=GameRead)
def get_game(game_id: str):
    svc = GameService()
    item = svc.get(game_id)
    if not item:
        raise HTTPException(404, "Game not found")
    return item


@router.post(
    "",
    response_model=GameRead,
    status_code=201,
    dependencies=[
        Depends(require_admin),
    ],
)
def create_game(payload: GameCreate):
    svc = GameService()
    return svc.create(payload)


@router.patch(
    "/{game_id}",
    response_model=GameRead,
    dependencies=[Depends(require_admin)],
)
def update_game(game_id: str, payload: GameUpdate):
    svc = GameService()
    item = svc.update(game_id, payload)
    if not item:
        raise HTTPException(404, "Game not found")
    return item


@router.delete(
    "/{game_id}",
    status_code=204,
    dependencies=[Depends(require_admin)],
)
def delete_game(game_id: str):
    svc = GameService()
    ok = svc.delete(game_id)
    if not ok:
        raise HTTPException(404, "Game not found")
