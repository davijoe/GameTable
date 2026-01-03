from app.repository.video.video_repository_factory import get_video_repository
from app.schema.video_schema import VideoCreate, VideoRead, VideoUpdate


class VideoService:
    def __init__(self):
        self.repo = get_video_repository()

    def get(self, video_id: int) -> VideoRead | None:
        obj = self.repo.get(video_id)
        return VideoRead.model_validate(obj) if obj else None

    def list(
        self,
        offset: int = 0,
        limit: int = 50,
        search: str | None = None,
        sort_by: str | None = None,
    ) -> tuple[list[VideoRead], int]:
        rows, total = self.repo.list(offset, limit, search, sort_by)
        return [VideoRead.model_validate(r) for r in rows], total

    def create(self, payload: VideoCreate) -> VideoRead:
        obj = self.repo.create(payload.model_dump())
        return VideoRead.model_validate(obj)

    def update(self, video_id: int, payload: VideoUpdate) -> VideoRead | None:
        obj = self.repo.update(video_id, payload.model_dump(exclude_unset=True))
        return VideoRead.model_validate(obj) if obj else None

    def delete(self, video_id: int) -> bool:
        return self.repo.delete(video_id)
