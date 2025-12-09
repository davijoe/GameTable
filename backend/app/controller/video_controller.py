from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schema.video_schema import VideoCreate, VideoRead, VideoUpdate
from app.service.video_service import VideoService
from app.utility.auth import require_admin
from app.utility.db_sql import get_sql_db

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.get("", response_model=dict[str, Any])
def list_videos(
    q: str | None = Query(None, description="Search by title"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_sql_db),
):
    svc = VideoService(db)
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post(
    "",
    response_model=VideoRead,
    status_code=201,
    dependencies=[Depends(require_admin)],
)
def create_video(payload: VideoCreate, db: Session = Depends(get_sql_db)):
    svc = VideoService(db)
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{video_id}", response_model=VideoRead)
def get_video(video_id: int, db: Session = Depends(get_sql_db)):
    svc = VideoService(db)
    item = svc.get(video_id)
    if not item:
        raise HTTPException(status_code=404, detail="Video not found")
    return item


@router.put(
    "/{video_id}",
    response_model=VideoRead,
    dependencies=[Depends(require_admin)],
)
def update_video(
    video_id: int, payload: VideoUpdate, db: Session = Depends(get_sql_db)
):
    svc = VideoService(db)
    try:
        item = svc.update(video_id, payload)
        if not item:
            raise HTTPException(status_code=404, detail="Video not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{video_id}",
    status_code=204,
    dependencies=[Depends(require_admin)],
)
def delete_video(video_id: int, db: Session = Depends(get_sql_db)):
    svc = VideoService(db)
    if not svc.delete(video_id):
        raise HTTPException(status_code=404, detail="Video not found")
