from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.model.artists_model import Artists
from app.schema.artist_schema import ArtistCreate, ArtistRead, ArtistUpdate
from app.repository.sql.sql_artist_repository import SQLArtistRepository


class ArtistService:
    def __init__(self, db: Session):
        self.repo = SQLArtistRepository(db)
        self.db = db

    def get(self, artist_id: int) -> Optional[ArtistRead]:
        obj = self.repo.get(artist_id)
        return ArtistRead.model_validate(obj) if obj else None

    def list(
        self, offset: int, limit: int, search: Optional[str]
    ) -> Tuple[List[ArtistRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [ArtistRead.model_validate(r) for r in rows], total

    def create(self, payload: ArtistCreate) -> ArtistRead:
        if self.repo.get_by_name(payload.name):
            raise ValueError("Artist with this name already exists")

        obj = Artists(**payload.model_dump())
        obj = self.repo.create(obj)
        self.db.commit()
        self.db.refresh(obj)
        return ArtistRead.model_validate(obj)

    def update(self, artist_id: int, payload: ArtistUpdate) -> Optional[ArtistRead]:
        obj = self.repo.get(artist_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)

        if "name" in update_data:
            existing = self.repo.get_by_name(update_data["name"])
            if existing and existing.id != artist_id:
                raise ValueError("Artist with this name already exists")

        for key, value in update_data.items():
            setattr(obj, key, value)

        obj = self.repo.update(obj)
        self.db.commit()
        self.db.refresh(obj)
        return ArtistRead.model_validate(obj)

    def delete(self, artist_id: int) -> bool:
        obj = self.repo.get(artist_id)
        if not obj:
            return False
        self.repo.delete(obj)
        self.db.commit()
        return True

