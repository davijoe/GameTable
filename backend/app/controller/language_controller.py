from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schema.language_schema import LanguageCreate, LanguageRead, LanguageUpdate
from app.service.language_service import LanguageService
from app.utility.auth import require_admin
from app.utility.db_sql import get_sql_db

router = APIRouter(prefix="/api/languages", tags=["languages"])


@router.get("", response_model=dict[str, Any])
def list_languages(
    q: str | None = Query(None, description="Search by language name"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_sql_db),
):
    svc = LanguageService(db)
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post(
    "",
    response_model=LanguageRead,
    status_code=201,
    dependencies=[Depends(require_admin)],
)
def create_language(payload: LanguageCreate, db: Session = Depends(get_sql_db)):
    svc = LanguageService(db)
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{language_id}", response_model=LanguageRead)
def get_language(language_id: int, db: Session = Depends(get_sql_db)):
    svc = LanguageService(db)
    item = svc.get(language_id)
    if not item:
        raise HTTPException(status_code=404, detail="Language not found")
    return item


@router.put(
    "/{language_id}",
    response_model=LanguageRead,
    dependencies=[Depends(require_admin)],
)
def update_language(
    language_id: int, payload: LanguageUpdate, db: Session = Depends(get_sql_db)
):
    svc = LanguageService(db)
    try:
        item = svc.update(language_id, payload)
        if not item:
            raise HTTPException(status_code=404, detail="Language not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{language_id}",
    status_code=204,
    dependencies=[Depends(require_admin)],
)
def delete_language(language_id: int, db: Session = Depends(get_sql_db)):
    svc = LanguageService(db)
    try:
        if not svc.delete(language_id):
            raise HTTPException(status_code=404, detail="Language not found")
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
