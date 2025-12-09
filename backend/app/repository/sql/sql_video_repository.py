from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.video_model import Video


class SQLVideoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, video_id: int) -> Video | None:
        return self.db.get(Video, video_id)

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[Video], int]:
        stmt = select(Video)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(Video.title.ilike(like))
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, video: Video) -> Video:
        self.db.add(video)
        self.db.commit()
        return video

    def update(self, video: Video) -> Video:
        self.db.merge(video)
        self.db.commit()
        return video

    def delete(self, video: Video) -> None:
        self.db.delete(video)
        self.db.commit()
