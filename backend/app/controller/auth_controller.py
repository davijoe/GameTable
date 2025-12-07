from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schema.auth_schema import LoginRequest, LoginResponse
from app.service.user_service import UserService
from app.utility.auth import create_access_token
from app.utility.db_sql import get_sql_db

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_sql_db)):
    svc = UserService(db)
    user = svc.authenticate(payload.username, payload.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user_id=user.id, username=user.username)

    return LoginResponse(
        access_token=token,
        user_id=user.id,
        username=user.username,
        display_name=user.display_name,
    )


@router.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_sql_db),
):
    svc = UserService(db)
    user = svc.authenticate(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(user_id=user.id, username=user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
