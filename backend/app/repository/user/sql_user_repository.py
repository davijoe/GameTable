from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.user_model import User
from app.repository.user.i_user_repository import IUserRepository


class UserRepositorySQL(IUserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.db.execute(stmt).scalars().first()

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalars().first()

    def list(self, offset: int, limit: int, search: str | None):
        stmt = select(User)
        if search:
            like = f"%{search}%"
            stmt = stmt.where((User.username.ilike(like)) | (User.email.ilike(like)))

        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, user_data: dict) -> User:
        obj = User(**user_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, user_id: int, user_data: dict) -> User | None:
        obj = self.get(user_id)
        if not obj:
            return None
        for k, v in user_data.items():
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, user_id: int) -> bool:
        obj = self.get(user_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
