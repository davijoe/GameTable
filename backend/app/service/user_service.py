from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.model.user_model import User
from app.repository.user_repository import UserRepository
from app.schema.user_schema import UserCreate, UserRead, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

    def get(self, user_id: int) -> Optional[UserRead]:
        obj = self.repo.get(user_id)
        return UserRead.model_validate(obj) if obj else None

    def get_by_username(self, username: str) -> Optional[UserRead]:
        obj = self.repo.get_by_username(username)
        return UserRead.model_validate(obj) if obj else None

    def get_by_email(self, email: str) -> Optional[UserRead]:
        obj = self.repo.get_by_email(email)
        return UserRead.model_validate(obj) if obj else None

    def list(
        self, offset: int, limit: int, search: Optional[str]
    ) -> Tuple[List[UserRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [UserRead.model_validate(r) for r in rows], total

    def create(self, payload: UserCreate) -> UserRead:
        # Here you would typically hash the password before storing
        # TODO: Add password hashing
        obj = User(**payload.model_dump())
        obj = self.repo.create(obj)
        self.db.commit()
        self.db.refresh(obj)
        return UserRead.model_validate(obj)

    def update(self, user_id: int, payload: UserUpdate) -> Optional[UserRead]:
        obj = self.repo.get(user_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        # Here you would typically hash the password if it's being updated
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

