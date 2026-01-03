from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schema.publisher_schema import PublisherCreate, PublisherRead, PublisherUpdate
from app.service.publisher_service import PublisherService
from app.utility.auth import require_admin
from app.utility.db_sql import get_sql_db

router = APIRouter(prefix="/api/publishers", tags=["publishers"])


@router.get("", response_model=dict[str, Any])
def list_publishers(
    q: str | None = Query(None, description="Search by publisher name"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_sql_db),
):
    svc = PublisherService()
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post(
    "",
    response_model=PublisherRead,
    status_code=201,
    dependencies=[Depends(require_admin)],
)
def create_publisher(payload: PublisherCreate, db: Session = Depends(get_sql_db)):
    svc = PublisherService()
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{publisher_id}", response_model=PublisherRead)
def get_publisher(publisher_id: int, db: Session = Depends(get_sql_db)):
    svc = PublisherService()
    item = svc.get(publisher_id)
    if not item:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return item


@router.patch(
    "/{publisher_id}",
    response_model=PublisherRead,
    dependencies=[Depends(require_admin)],
)
def update_publisher(
    publisher_id: int, payload: PublisherUpdate, db: Session = Depends(get_sql_db)
):
    svc = PublisherService()
    try:
        item = svc.update(publisher_id, payload)
        if not item:
            raise HTTPException(status_code=404, detail="Publisher not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{publisher_id}",
    status_code=204,
    dependencies=[Depends(require_admin)],
)
def delete_publisher(publisher_id: int, db: Session = Depends(get_sql_db)):
    svc = PublisherService()
    if not svc.delete(publisher_id):
        raise HTTPException(status_code=404, detail="Publisher not found")
