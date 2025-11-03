from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.utility.db import get_db
from app.schema.genre_schema import GenreRead, GenreCreate, GenreUpdate
from app.service.genre_service import GenreService

router = APIRouter(prefix="/api/genres", tags=["genres"])


@router.get("", response_model=Dict[str, Any])
def list_genres(
    q: Optional[str] = Query(None, description="Search by title"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    svc = GenreService(db)
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post("", response_model=GenreRead)
def create_genre(payload: GenreCreate, db: Session = Depends(get_db)):
    svc = GenreService(db)
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{genre_id}", response_model=GenreRead)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    svc = GenreService(db)
    item = svc.get(genre_id)
    if not item:
        raise HTTPException(status_code=404, detail="Genre not found")
    return item


@router.put("/{genre_id}", response_model=GenreRead)
def update_genre(genre_id: int, payload: GenreUpdate, db: Session = Depends(get_db)):
    svc = GenreService(db)
    try:
        item = svc.update(genre_id, payload)
        if not item:
            raise HTTPException(status_code=404, detail="Genre not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{genre_id}", status_code=204)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    svc = GenreService(db)
    if not svc.delete(genre_id):
        raise HTTPException(status_code=404, detail="Genre not found")