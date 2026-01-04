from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.publisher_model import Publisher
from app.repository.publisher.i_publisher_repository import IPublisherRepository


class PublisherRepositorySQL(IPublisherRepository):
    def __init__(self, db: Session):
        self.db = db

    def get(self, publisher_id: int) -> Publisher | None:
        return self.db.get(Publisher, publisher_id)

    def get_by_name(self, name: str) -> Publisher | None:
        stmt = select(Publisher).where(Publisher.name == name)
        return self.db.execute(stmt).scalars().first()

    def list(
        self,
        offset: int,
        limit: int,
        search: str | None,
        sort_by: str | None,
        sort_order: str | None = "asc",
    ) -> tuple[list[Publisher], int]:
        stmt = select(Publisher)

        if search:
            stmt = stmt.where(Publisher.name.ilike(f"%{search}%"))

        # whitelist sorting
        if sort_by == "name" or not sort_by:
            col = Publisher.name
            stmt = stmt.order_by(
                col.asc() if (sort_order or "asc") == "asc" else col.desc()
            )
        else:
            stmt = stmt.order_by(Publisher.name.asc())

        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, publisher_data: dict) -> Publisher:
        obj = Publisher(**publisher_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, publisher_id: int, publisher_data: dict) -> Publisher | None:
        obj = self.get(publisher_id)
        if not obj:
            return None

        for k, v in publisher_data.items():
            setattr(obj, k, v)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, publisher_id: int) -> bool:
        obj = self.get(publisher_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
