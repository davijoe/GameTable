from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schema.designer_schema import DesignerCreate, DesignerRead, DesignerUpdate
from app.service.designer_service import DesignerService
from app.utility.db import get_db

router = APIRouter(prefix="/api/designers", tags=["designers"])


@router.get("", response_model=Dict[str, Any])
def list_designers(
    q: Optional[str] = Query(None, description="Search by name"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    svc = DesignerService(db)
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post("", response_model=DesignerRead)
def create_designer(payload: DesignerCreate, db: Session = Depends(get_db)):
    svc = DesignerService(db)
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{designer_id}", response_model=DesignerRead)
def get_designer(designer_id: int, db: Session = Depends(get_db)):
    svc = DesignerService(db)
    item = svc.get(designer_id)
    if not item:
        raise HTTPException(status_code=404, detail="Designer not found")
    return item


@router.put("/{designer_id}", response_model=DesignerRead)
def update_designer(
    designer_id: int, payload: DesignerUpdate, db: Session = Depends(get_db)
):
    svc = DesignerService(db)
    try:
        item = svc.update(designer_id, payload)
        if not item:
            raise HTTPException(status_code=404, detail="Designer not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{designer_id}", status_code=204)
def delete_designer(designer_id: int, db: Session = Depends(get_db)):
    svc = DesignerService(db)
    if not svc.delete(designer_id):
        raise HTTPException(status_code=404, detail="Designer not found")

