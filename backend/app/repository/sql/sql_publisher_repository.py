from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.publisher_model import Publisher


class SQLPublisherRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, publisher_id: int) -> Publisher | None:
        return self.db.get(Publisher, publisher_id)

    def get_by_name(self, name: str) -> Publisher | None:
        return self.db.execute(select(Publisher).where(Publisher.name == name)).scalar_one_or_none()

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[Publisher], int]:
        stmt = select(Publisher)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(Publisher.name.ilike(like))
        total = self.db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, publisher: Publisher) -> Publisher:
        self.db.add(publisher)
        self.db.commit()
        return publisher

    def update(self, publisher: Publisher) -> Publisher:
        self.db.merge(publisher)
        self.db.commit()
        return publisher

    def delete(self, publisher: Publisher) -> None:
        self.db.delete(publisher)
        self.db.commit()
