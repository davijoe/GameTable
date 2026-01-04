from app.repository.publisher.publisher_repository_factory import (
    get_publisher_repository,
)
from app.schema.publisher_schema import PublisherCreate, PublisherRead, PublisherUpdate


class PublisherService:
    def __init__(self):
        self.repo = get_publisher_repository()

    def get(self, publisher_id: int) -> PublisherRead | None:
        obj = self.repo.get(publisher_id)
        return PublisherRead.model_validate(obj) if obj else None

    def list(
        self,
        offset: int = 0,
        limit: int = 50,
        search: str | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
    ) -> tuple[list[PublisherRead], int]:
        rows, total = self.repo.list(
            offset,
            limit,
            search,
            sort_by,
            sort_order,
        )
        return [PublisherRead.model_validate(r) for r in rows], total

    def create(self, payload: PublisherCreate) -> PublisherRead:
        if self.repo.get_by_name(payload.name):
            raise ValueError("Publisher with this name already exists")

        obj = self.repo.create(payload.model_dump())
        return PublisherRead.model_validate(obj)

    def update(
        self, publisher_id: int, payload: PublisherUpdate
    ) -> PublisherRead | None:
        update_data = payload.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing = self.repo.get_by_name(update_data["name"])
            if existing and existing.id != publisher_id:
                raise ValueError("Publisher with this name already exists")

        obj = self.repo.update(publisher_id, update_data)
        return PublisherRead.model_validate(obj) if obj else None

    def delete(self, publisher_id: int) -> bool:
        obj = self.repo.get(publisher_id)
        if not obj:
            return False
        return True
