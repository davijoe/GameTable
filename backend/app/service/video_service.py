from sqlalchemy.orm import Session

from app.model.video_model import Video
from app.repository.sql.sql_video_repository import SQLVideoRepository
from app.schema.video_schema import VideoCreate, VideoRead, VideoUpdate


class VideoService:
    def __init__(self, db: Session):
        self.repo = SQLVideoRepository(db)
        self.db = db

    def get(self, video_id: int) -> VideoRead | None:
        obj = self.repo.get(video_id)
        return VideoRead.model_validate(obj) if obj else None

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[VideoRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [VideoRead.model_validate(r) for r in rows], total

    def create(self, payload: VideoCreate) -> VideoRead:
        video = Video(**payload.model_dump())
        video = self.repo.create(video)
        self.db.commit()
        self.db.refresh(video)
        return VideoRead.model_validate(video)

    def update(self, video_id: int, payload: VideoUpdate) -> VideoRead | None:
        obj = self.repo.get(video_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)

        obj = self.repo.update(obj)
        self.db.commit()
        self.db.refresh(obj)
        return VideoRead.model_validate(obj)

    def delete(self, video_id: int) -> bool:
        obj = self.repo.get(video_id)
        if not obj:
            return False
        self.repo.delete(obj)
        self.db.commit()
        return True
