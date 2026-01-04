from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query

from app.schema.artist_schema import ArtistCreate, ArtistRead, ArtistUpdate
from app.service.artist_service import ArtistService
from app.utility.auth import require_admin

router = APIRouter(prefix="/api/artists", tags=["artists"])


@router.get("", response_model=dict[str, Any])
def list_artists(
    q: str | None = Query(None, description="Search by name"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    svc = ArtistService()
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post(
    "",
    response_model=ArtistRead,
    dependencies=[Depends(require_admin)],
)
def create_artist(
    payload: ArtistCreate,
):
    svc = ArtistService()
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{artist_id}", response_model=ArtistRead)
def get_artist(
    artist_id: int,
):
    svc = ArtistService()
    item = svc.get(artist_id)
    if not item:
        raise HTTPException(status_code=404, detail="Artist not found")
    return item


@router.patch(
    "/{artist_id}",
    response_model=ArtistRead,
    dependencies=[Depends(require_admin)],
)
def update_artist(
    artist_id: int, payload: ArtistUpdate
):
    svc = ArtistService()
    try:
        item = svc.update(artist_id, payload)
        if not item:
            raise HTTPException(status_code=404, detail="Artist not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{artist_id}",
    status_code=204,
    dependencies=[Depends(require_admin)],
)
def delete_artist(
    artist_id: int,
):
    svc = ArtistService()
    if not svc.delete(artist_id):
        raise HTTPException(status_code=404, detail="Artist not found")
