from typing import Any

from fastapi import APIRouter, HTTPException

# from sqlalchemy.orm import Session
from app.schema.game_schema import GameCreate, GameRead, GameUpdate
from app.service.game_service import GameService

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


@router.get("/{game_id}", response_model=GameRead)
def get_game(game_id: str):
    svc = GameService()
    item = svc.get(game_id)
    if not item:
        raise HTTPException(404, "Game not found")
    return item


@router.post("", response_model=GameRead, status_code=201)
def create_game(payload: GameCreate):
    svc = GameService()
    return svc.create(payload)


@router.patch("/{game_id}", response_model=GameRead)
def update_game(game_id: str, payload: GameUpdate):
    svc = GameService()
    item = svc.update(game_id, payload)
    if not item:
        raise HTTPException(404, "Game not found")
    return item


@router.delete("/{game_id}", status_code=204)
def delete_game(game_id: str):
    svc = GameService()
    ok = svc.delete(game_id)
    if not ok:
        raise HTTPException(404, "Game not found")


# old controller before new architecture - graveyard because might use for descriptions or other?
"""
@router.get("", response_model=Dict[str, Any])
def list_games(
    q: Optional[str] = Query(None, description="Search by name"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    svc = GameService(db)
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.get("/{game_id}", response_model=GameRead)
def get_game(game_id: int, db: Session = Depends(get_db)):
    svc = GameService(db)
    item = svc.get(game_id)
    if not item:
        raise HTTPException(status_code=404, detail="Game not found")
    return item


@router.post("", response_model=GameRead, status_code=201)
def create_game(payload: GameCreate, db: Session = Depends(get_db)):
    svc = GameService(db)
    return svc.create(payload)


@router.patch("/{game_id}", response_model=GameRead)
def update_game(game_id: int, payload: GameUpdate, db: Session = Depends(get_db)):
    svc = GameService(db)
    item = svc.update(game_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Game not found")
    return item


@router.delete("/{game_id}", status_code=204)
def delete_game(game_id: int, db: Session = Depends(get_db)):
    svc = GameService(db)
    ok = svc.delete(game_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Game not found")
"""

