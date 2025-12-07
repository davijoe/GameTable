from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.model.user_model import User
from app.schema.user_schema import UserCreate, UserRead, UserUpdate
from app.service.user_service import UserService
from app.utility.auth import get_current_user, require_admin
from app.utility.db_sql import get_sql_db

router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/api/users")
def list_users(
    q: str | None = Query(
        None,
        description="Search by display name or username",
    ),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_sql_db),
):
    svc = UserService(db)
    items, total = svc.list(offset=offset, limit=limit, search=q)
    return {"total": total, "offset": offset, "limit": limit, "items": items}


@router.post(
    "/api/users",
    response_model=UserRead,
)
def create_user(payload: UserCreate, db: Session = Depends(get_sql_db)):
    svc = UserService(db)

    if svc.get_by_username(payload.username):
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )

    if svc.get_by_email(payload.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    return svc.create(payload)


@router.get(
    "/api/user/{user_id}",
    response_model=UserRead,
)
def get_user(user_id: int, db: Session = Depends(get_sql_db)):
    svc = UserService(db)
    item = svc.get(user_id)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item


@router.put("/api/user/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_sql_db),
):
    svc = UserService(db)

    if payload.username is not None:
        existing_user = svc.get_by_username(payload.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="Username already taken",
            )

    if payload.email is not None:
        existing_user = svc.get_by_email(payload.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=400,
                detail="Email already registered",
            )

    item = svc.update(user_id, payload)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item


@router.delete(
    "/api/user/{user_id}",
    status_code=204,
    dependencies=[
        Depends(require_admin),
    ],
)
def delete_user(user_id: int, db: Session = Depends(get_sql_db)):
    svc = UserService(db)
    if not svc.delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")
