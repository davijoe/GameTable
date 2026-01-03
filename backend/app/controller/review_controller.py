from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schema.review_schema import ReviewCreate, ReviewRead, ReviewUpdate
from app.service.review_service import ReviewService
from app.utility.auth import require_admin
from app.utility.db_sql import get_sql_db

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.get("", response_model=dict[str, Any])
def list_reviews(
    q: str | None = Query(None, description="Search by title"),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_sql_db),
):
    svc = ReviewService()
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.get("/count", response_model=dict[str, int])
def get_review_count_for_game(
    game_id: int = Query(..., description="ID of the game"),
    db: Session = Depends(get_sql_db),
):
    svc = ReviewService()
    count = svc.get_review_count_for_game(game_id)
    return {"game_id": game_id, "review_count": count}


@router.get("/gameid/{game_id}", response_model=dict[str, Any])
def list_reviews_by_game(
    game_id: int,
    offset: int = Query(0, ge=0),
    limit: int = Query(5, ge=1),
    db: Session = Depends(get_sql_db),
):
    svc = ReviewService()
    items, total = svc.list_by_game(game_id=game_id, offset=offset, limit=limit)

    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post(
    "",
    response_model=ReviewRead,
    status_code=201,
    dependencies=[Depends(require_admin)],
)
def create_review(payload: ReviewCreate, db: Session = Depends(get_sql_db)):
    svc = ReviewService()
    try:
        return svc.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{review_id}", response_model=ReviewRead)
def get_review(review_id: int, db: Session = Depends(get_sql_db)):
    svc = ReviewService()
    item = svc.get(review_id)
    if not item:
        raise HTTPException(status_code=404, detail="Review not found")
    return item


@router.patch(
    "/{review_id}",
    response_model=ReviewRead,
    dependencies=[Depends(require_admin)],
)
def update_review(
    review_id: int, payload: ReviewUpdate, db: Session = Depends(get_sql_db)
):
    svc = ReviewService()
    try:
        item = svc.update(review_id, payload)
        if not item:
            raise HTTPException(status_code=404, detail="Review not found")
        return item
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete(
    "/{review_id}",
    status_code=204,
    dependencies=[Depends(require_admin)],
)
def delete_review(review_id: int, db: Session = Depends(get_sql_db)):
    svc = ReviewService()
    if not svc.delete(review_id):
        raise HTTPException(status_code=404, detail="Review not found")
