import hashlib

from sqlalchemy.orm import Session

from app.model.user_model import User
from app.repository.sql.sql_user_repository import SQLUserRepository
from app.schema.user_schema import UserCreate, UserRead, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repo = SQLUserRepository(db)
        self.db = db

    def get(self, user_id: int) -> UserRead | None:
        obj = self.repo.get(user_id)
        return UserRead.model_validate(obj) if obj else None

    def get_by_username(self, username: str) -> UserRead | None:
        obj = self.repo.get_by_username(username)
        return UserRead.model_validate(obj) if obj else None

    def get_by_email(self, email: str) -> UserRead | None:
        obj = self.repo.get_by_email(email)
        return UserRead.model_validate(obj) if obj else None

    def list(
        self, offset: int, limit: int, search: str | None
    ) -> tuple[list[UserRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [UserRead.model_validate(r) for r in rows], total

    def create(self, payload: UserCreate) -> UserRead:
        # Here we should hash the password before storing
        # TODO: Add password hashing
        obj = User(**payload.model_dump())
        obj = self.repo.create(obj)
        self.db.commit()
        self.db.refresh(obj)
        return UserRead.model_validate(obj)

    def update(self, user_id: int, payload: UserUpdate) -> UserRead | None:
        obj = self.repo.get(user_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        # Here we should hash the password if it's being updated
        # TODO: Add password hashing if password is in update_data

        for key, value in update_data.items():
            setattr(obj, key, value)

        obj = self.repo.update(obj)
        self.db.commit()
        self.db.refresh(obj)
        return UserRead.model_validate(obj)

    def delete(self, user_id: int) -> bool:
        obj = self.repo.get(user_id)
        if not obj:
            return False
        self.repo.delete(obj)
        self.db.commit()
        return True

    def authenticate(self, username: str, password: str) -> UserRead | None:
        """Authenticate a user by username and password.

        Returns the user if credentials are valid, None otherwise.
        Password in database is hashed with SHA256.
        """
        user = self.repo.get_by_username(username)
        if not user:
            return None

        # Hash the input password and compare with database password
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        if hashed_input != user.password:
            return None

        return UserRead.model_validate(user)
