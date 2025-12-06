from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.schema.auth_schema import LoginRequest, LoginResponse
from app.schema.user_schema import UserCreate, UserRead, UserUpdate
from app.service.user_service import UserService
from app.utility.auth import create_access_token
from app.utility.db_sql import get_sql_db

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/auth/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_sql_db)):
    """Authenticate user and return JWT token."""
    svc = UserService(db)
    user = svc.authenticate(payload.username, payload.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user_id=user.id, username=user.username)

    return LoginResponse(
        access_token=access_token,
        user_id=user.id,
        username=user.username,
        display_name=user.display_name,
    )


@router.get("")
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


@router.post("", response_model=UserRead)
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


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_sql_db)):
    svc = UserService(db)
    item = svc.get(user_id)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")
    return item


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_sql_db)):
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


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_sql_db)):
    svc = UserService(db)
    if not svc.delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")
