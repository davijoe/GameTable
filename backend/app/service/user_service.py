import bcrypt
from sqlalchemy.orm import Session

from app.model.user_model import User
from app.repository.sql.sql_user_repository import SQLUserRepository
from app.schema.user_schema import UserCreate, UserRead, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repo = SQLUserRepository(db)
        self.db = db

    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def _verify_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

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
        data = payload.model_dump()
        data["password"] = self._hash_password(data["password"])

        obj = User(**data)
        obj = self.repo.create(obj)
        self.db.commit()
        self.db.refresh(obj)
        return UserRead.model_validate(obj)

    def update(self, user_id: int, payload: UserUpdate) -> UserRead | None:
        obj = self.repo.get(user_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = self._hash_password(update_data["password"])

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

    def authenticate(self, username: str, password: str):
        user = self.repo.get_by_username(username)
        if not user:
            return None

        if not self._verify_password(password, user.password):
            return None

        return UserRead.model_validate(user)
