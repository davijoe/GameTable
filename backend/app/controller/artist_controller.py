from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.utility.db import get_db
from app.schema.artist_schema import ArtistRead, ArtistCreate, ArtistUpdate
from app.service.artist_service import ArtistService

router = APIRouter(prefix="/api/artists", tags=["artists"])


@router.get("", response_model=Dict[str, Any])
def list_artists(
    q: Optional[str] = Query(None, description="Search by name"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    svc = ArtistService(db)
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post("", response_model=ArtistRead)
def create_artist(payload: ArtistCreate, db: Session = Depends(get_db)):
    svc = ArtistService(db)
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{artist_id}", response_model=ArtistRead)
def get_artist(artist_id: int, db: Session = Depends(get_db)):
    svc = ArtistService(db)
    item = svc.get(artist_id)
    if not item:
        raise HTTPException(status_code=404, detail="Artist not found")
    return item


@router.put("/{artist_id}", response_model=ArtistRead)
def update_artist(artist_id: int, payload: ArtistUpdate, db: Session = Depends(get_db)):
    svc = ArtistService(db)
    try:
        item = svc.update(artist_id, payload)
        if not item:
            raise HTTPException(status_code=404, detail="Artist not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{artist_id}", status_code=204)
def delete_artist(artist_id: int, db: Session = Depends(get_db)):
    svc = ArtistService(db)
    if not svc.delete(artist_id):
        raise HTTPException(status_code=404, detail="Artist not found")

