from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.utility.db import get_db
from app.schema.matchup_schema import MatchupRead, MatchupCreate, MatchupUpdate
from app.service.matchup_service import MatchupService

router = APIRouter(prefix="/api/matchups", tags=["matchups"])


@router.get("", response_model=Dict[str, Any])
def list_matchups(
    game_id: Optional[int] = Query(None, description="Filter by game ID"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    svc = MatchupService(db)
    items, total = svc.list(offset=offset, limit=limit, game_id=game_id)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post("", response_model=MatchupRead)
def create_matchup(payload: MatchupCreate, db: Session = Depends(get_db)):
    svc = MatchupService(db)
    return svc.create(payload)


@router.get("/{matchup_id}", response_model=MatchupRead)
def get_matchup(matchup_id: int, db: Session = Depends(get_db)):
    svc = MatchupService(db)
    item = svc.get(matchup_id)
    if not item:
        raise HTTPException(status_code=404, detail="Matchup not found")
    return item


@router.put("/{matchup_id}", response_model=MatchupRead)
def update_matchup(matchup_id: int, payload: MatchupUpdate, db: Session = Depends(get_db)):
    svc = MatchupService(db)
    item = svc.update(matchup_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Matchup not found")
    return item


@router.delete("/{matchup_id}", status_code=204)
def delete_matchup(matchup_id: int, db: Session = Depends(get_db)):
    svc = MatchupService(db)
    if not svc.delete(matchup_id):
        raise HTTPException(status_code=404, detail="Matchup not found")


@router.get("/user/{user_id}", response_model=Dict[str, Any])
def get_user_matchups(
    user_id: int,
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    svc = MatchupService(db)
    items, total = svc.get_user_matchups(user_id=user_id, offset=offset, limit=limit)
    return {"total": total, "offset": offset, "limit": limit, "items": items}