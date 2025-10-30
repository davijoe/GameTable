from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from app.model.designer_model import Designer
from app.schema.designer_schema import DesignerCreate, DesignerUpdate, DesignerRead
from app.repository.designer_repository import DesignerRepository


class DesignerService:
    def __init__(self, db: Session):
        self.repo = DesignerRepository(db)
        self.db = db

    def get(self, designer_id: int) -> Optional[DesignerRead]:
        obj = self.repo.get(designer_id)
        return DesignerRead.model_validate(obj) if obj else None

    def list(
        self, offset: int, limit: int, search: Optional[str]
    ) -> Tuple[List[DesignerRead], int]:
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

    def update(self, designer_id: int, payload: DesignerUpdate) -> Optional[DesignerRead]:
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