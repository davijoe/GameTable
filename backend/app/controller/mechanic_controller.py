from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schema.mechanic_schema import MechanicCreate, MechanicRead, MechanicUpdate
from app.service.mechanic_service import MechanicService
from app.utility.auth import require_admin
from app.utility.db_sql import get_sql_db

router = APIRouter(prefix="/api/mechanics", tags=["mechanics"])


@router.get("", response_model=dict[str, Any])
def list_mechanics(
    q: str | None = Query(None, description="Search by mechanic name"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_sql_db),
):
    svc = MechanicService(db)
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post(
    "",
    response_model=MechanicRead,
    status_code=201,
    dependencies=[Depends(require_admin)],
)
def create_mechanic(payload: MechanicCreate, db: Session = Depends(get_sql_db)):
    svc = MechanicService(db)
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{mechanic_id}", response_model=MechanicRead)
def get_mechanic(mechanic_id: int, db: Session = Depends(get_sql_db)):
    svc = MechanicService(db)
    item = svc.get(mechanic_id)
    if not item:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    return item


@router.patch(
    "/{mechanic_id}",
    response_model=MechanicRead,
    dependencies=[Depends(require_admin)],
)
def update_mechanic(
    mechanic_id: int, payload: MechanicUpdate, db: Session = Depends(get_sql_db)
):
    svc = MechanicService(db)
    try:
        item = svc.update(mechanic_id, payload)
        if not item:
            raise HTTPException(status_code=404, detail="Mechanic not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{mechanic_id}",
    status_code=204,
    dependencies=[Depends(require_admin)],
)
def delete_mechanic(mechanic_id: int, db: Session = Depends(get_sql_db)):
    svc = MechanicService(db)
    if not svc.delete(mechanic_id):
        raise HTTPException(status_code=404, detail="Mechanic not found")
