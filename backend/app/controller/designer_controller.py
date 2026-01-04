from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schema.designer_schema import (
    DesignerCreate,
    DesignerRead,
    DesignerUpdate,
)
from app.service.designer_service import DesignerService
from app.utility.auth import require_admin
from app.utility.db_sql import get_sql_db

router = APIRouter(prefix="/api/designers", tags=["designers"])


@router.get("", response_model=dict[str, Any])
def list_designers(
    q: str | None = Query(None, description="Search by name"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    svc = DesignerService()
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post(
    "",
    response_model=DesignerRead,
    dependencies=[Depends(require_admin)],
)
def create_designer(
    payload: DesignerCreate,
):
    svc = DesignerService()
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{designer_id}", response_model=DesignerRead)
def get_designer(designer_id: int):
    svc = DesignerService()
    item = svc.get(designer_id)
    if not item:
        raise HTTPException(status_code=404, detail="Designer not found")
    return item


@router.patch(
    "/{designer_id}",
    response_model=DesignerRead,
    dependencies=[Depends(require_admin)],
)
def update_designer(
    designer_id: int,
    payload: DesignerUpdate,
):
    svc = DesignerService()
    try:
        item = svc.update(designer_id, payload)
        if not item:
            raise HTTPException(status_code=404, detail="Designer not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{designer_id}",
    status_code=204,
    dependencies=[Depends(require_admin)],
)
def delete_designer(
    designer_id: int,
):
    svc = DesignerService()
    if not svc.delete(designer_id):
        raise HTTPException(status_code=404, detail="Designer not found")
