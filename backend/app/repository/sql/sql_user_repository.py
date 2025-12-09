from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.user_model import User


class SQLUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[User], int]:
        stmt = select(User)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(
                (User.display_name.ilike(like)) | (User.username.ilike(like))
            )
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()
        return user

    def update(self, user: User) -> User:
        self.db.merge(user)
        self.db.flush()
        return user

    def delete(self, user: User) -> bool:
        try:
            if not user:
                return False
            
            for review in user.reviews:
                self.db.delete(review)
            
            self.db.delete(user)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise
