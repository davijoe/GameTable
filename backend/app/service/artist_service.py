from sqlalchemy.orm import Session

from app.model.artists_model import Artist
from app.repository.artist.artist_repository_factory import get_artist_repository
from app.schema.artist_schema import ArtistCreate, ArtistRead, ArtistUpdate


class ArtistService:
    def __init__(self):
        self.repo = get_artist_repository()

    def get(self, artist_id: int) -> ArtistRead | None:
        obj = self.repo.get(artist_id)
        if not obj:
            return None
        return ArtistRead.model_validate(obj)

    def list(
        self, offset: int, limit: int, search: str | None
    ) -> tuple[list[ArtistRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [ArtistRead.model_validate(r) for r in rows], total

    def create(self, payload: ArtistCreate) -> ArtistRead:
        if self.repo.get_by_name(payload.name):
            raise ValueError("Artist with this name already exists")

        artist_obj = Artist(**payload.model_dump())
        artist_obj = self.repo.create(artist_obj)

        return ArtistRead.model_validate(artist_obj)

    def update(self, artist_id: int, payload: ArtistUpdate) -> ArtistRead | None:
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
        return ArtistRead.model_validate(obj) if obj else None

    def delete(self, artist_id: int) -> bool:
        return self.repo.delete(artist_id)
