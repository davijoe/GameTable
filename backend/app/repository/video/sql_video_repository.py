from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.video_model import Video
from app.repository.video.i_video_repository import IVideoRepository


class VideoRepositorySQL(IVideoRepository):
    SORT_FIELDS = {
        "title": Video.title.asc(),
        "created_at": getattr(Video, "created_at", None),
    }

    def __init__(self, db: Session):
        self.db = db

    def get(self, video_id: int) -> Video | None:
        return self.db.get(Video, video_id)

    def list(
        self,
        offset: int,
        limit: int,
        search: str | None,
        sort_by: str | None,
        sort_order: str | None = "asc",
    ) -> tuple[list[Video], int]:
        stmt = select(Video)

        if search:
            like = f"%{search}%"
            stmt = stmt.where(Video.title.ilike(like))

        if sort_by == "created_at" and getattr(Video, "created_at", None) is not None:
            col = Video.created_at
            stmt = stmt.order_by(col.asc() if sort_order == "asc" else col.desc())
        elif sort_by == "title":
            col = Video.title
            stmt = stmt.order_by(col.asc() if sort_order == "asc" else col.desc())
        else:
            stmt = stmt.order_by(Video.title.asc())

        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()

        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, video_data: dict) -> Video:
        obj = Video(**video_data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, video_id: int, video_data: dict) -> Video | None:
        obj = self.get(video_id)
        if not obj:
            return None

        for k, v in video_data.items():
            setattr(obj, k, v)

        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, video_id: int) -> bool:
        obj = self.get(video_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
