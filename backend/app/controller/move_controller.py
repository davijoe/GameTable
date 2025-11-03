from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schema.move_schema import MoveCreate, MoveRead, MoveUpdate
from app.service.move_service import MoveService
from app.utility.db import get_db

router = APIRouter(prefix="/api/moves", tags=["moves"])


@router.get("", response_model=Dict[str, Any])
def list_moves(
    ply: Optional[int] = Query(None, description="Filter by ply number"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    svc = MoveService(db)
    items, total = svc.list(offset=offset, limit=limit, ply=ply)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post("", response_model=MoveRead)
def create_move(payload: MoveCreate, db: Session = Depends(get_db)):
    svc = MoveService(db)
    return svc.create(payload)


@router.get("/{move_id}", response_model=MoveRead)
def get_move(move_id: int, db: Session = Depends(get_db)):
    svc = MoveService(db)
    item = svc.get(move_id)
    if not item:
        raise HTTPException(status_code=404, detail="Move not found")
    return item


@router.put("/{move_id}", response_model=MoveRead)
def update_move(move_id: int, payload: MoveUpdate, db: Session = Depends(get_db)):
    svc = MoveService(db)
    item = svc.update(move_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="Move not found")
    return item


@router.delete("/{move_id}", status_code=204)
def delete_move(move_id: int, db: Session = Depends(get_db)):
    svc = MoveService(db)
    if not svc.delete(move_id):
        raise HTTPException(status_code=404, detail="Move not found")

