from sqlalchemy.orm import Session

from app.model.publisher_model import Publisher
from app.repository.sql.sql_publisher_repository import SQLPublisherRepository
from app.schema.publisher_schema import PublisherCreate, PublisherRead, PublisherUpdate


class PublisherService:
    def __init__(self, db: Session):
        self.repo = SQLPublisherRepository(db)
        self.db = db

    def get(self, publisher_id: int) -> PublisherRead | None:
        obj = self.repo.get(publisher_id)
        return PublisherRead.model_validate(obj) if obj else None

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[PublisherRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [PublisherRead.model_validate(r) for r in rows], total

    def create(self, payload: PublisherCreate) -> PublisherRead:
        if self.repo.get_by_name(payload.name):
            raise ValueError("Publisher with this name already exists")

        obj = Publisher(**payload.model_dump())
        obj = self.repo.create(obj)
        self.db.commit()
        self.db.refresh(obj)
        return PublisherRead.model_validate(obj)

    def update(self, publisher_id: int, payload: PublisherUpdate) -> PublisherRead | None:
        obj = self.repo.get(publisher_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing = self.repo.get_by_name(update_data["name"])
            if existing and existing.id != publisher_id:
                raise ValueError("Publisher with this name already exists")

        for key, value in update_data.items():
            setattr(obj, key, value)

        obj = self.repo.update(obj)
        self.db.commit()
        self.db.refresh(obj)
        return PublisherRead.model_validate(obj)

    def delete(self, publisher_id: int) -> bool:
        obj = self.repo.get(publisher_id)
        if not obj:
            return False
        self.repo.delete(obj)
        self.db.commit()
        return True
