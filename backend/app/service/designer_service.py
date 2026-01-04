from sqlalchemy.orm import Session

from app.model.designer_model import Designer
from app.repository.artist.artist_repository_factory import get_artist_repository
from app.repository.designer.sql_designer_repository import SQLDesignerRepository
from app.schema.designer_schema import DesignerCreate, DesignerRead, DesignerUpdate
from app.repository.designer.designer_repository_factory import get_designer_repository


class DesignerService:
    def __init__(self):
        self.repo = get_designer_repository()

    def get(self, designer_id: int) -> DesignerRead | None:
        obj = self.repo.get(designer_id)
        return DesignerRead.model_validate(obj) if obj else None

    def list(
        self, offset: int, limit: int, search: str | None
    ) -> tuple[list[DesignerRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [DesignerRead.model_validate(r) for r in rows], total

    def create(self, payload: DesignerCreate) -> DesignerRead:
        if self.repo.get_by_name(payload.name):
            raise ValueError("Designer with this name already exists")

        obj = Designer(**payload.model_dump())
        obj = self.repo.create(obj)
        self.db.commit()
        self.db.refresh(obj)
        return DesignerRead.model_validate(obj)

    def update(self, designer_id: int, payload: DesignerUpdate) -> DesignerRead | None:
        obj = self.repo.get(designer_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing = self.repo.get_by_name(update_data["name"])
            if existing and existing.id != designer_id:
                raise ValueError("Designer with this name already exists")

        for key, value in update_data.items():
            setattr(obj, key, value)

        obj = self.repo.update(obj)
        self.db.commit()
        self.db.refresh(obj)
        return DesignerRead.model_validate(obj)

    def delete(self, designer_id: int) -> bool:
        obj = self.repo.get(designer_id)
        if not obj:
            return False
        self.repo.delete(obj)
        self.db.commit()
        return True
