from sqlalchemy.orm import Session

from app.model.review_model import Review
from app.repository.sql.sql_review_repository import SQLReviewRepository
from app.schema.review_schema import ReviewCreate, ReviewRead, ReviewUpdate


class ReviewService:
    def __init__(self, db: Session):
        self.repo = SQLReviewRepository(db)
        self.db = db

    def get(self, review_id: int) -> ReviewRead | None:
        obj = self.repo.get(review_id)
        return ReviewRead.model_validate(obj) if obj else None

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[ReviewRead], int]:
        rows, total = self.repo.list(offset=offset, limit=limit, search=search)
        return [ReviewRead.model_validate(r) for r in rows], total

    def create(self, payload: ReviewCreate) -> ReviewRead:
        review = Review(**payload.model_dump())
        review = self.repo.create(review)
        self.db.commit()
        self.db.refresh(review)
        return ReviewRead.model_validate(review)

    def update(self, review_id: int, payload: ReviewUpdate) -> ReviewRead | None:
        obj = self.repo.get(review_id)
        if not obj:
            return None

        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(obj, key, value)

        obj = self.repo.update(obj)
        self.db.commit()
        self.db.refresh(obj)
        return ReviewRead.model_validate(obj)

    def delete(self, review_id: int) -> bool:
        obj = self.repo.get(review_id)
        if not obj:
            return False
        self.repo.delete(obj)
        self.db.commit()
        return True
