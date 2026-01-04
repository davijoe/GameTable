from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.model.review_model import Review
from app.repository.review.i_review_repository import IReviewRepository
from app.schema.review_schema import ReviewCreate  # only if you want to reuse it


class ReviewRepositorySQL(IReviewRepository):
    def __init__(self, db: Session):
        self.db = db

    def get(self, review_id: int) -> Review | None:
        return self.db.get(Review, review_id)

    def get_review_count_for_game(self, game_id: int) -> int:
        stmt = select(func.count()).select_from(Review).where(Review.game_id == game_id)
        return self.db.execute(stmt).scalar_one()

    def list_by_game(self, game_id: int, offset: int, limit: int):
        stmt = (
            select(Review).where(Review.game_id == game_id).order_by(Review.id.desc())
        )
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def list(self, offset: int, limit: int, search: str | None):
        stmt = select(Review)
        if search:
            stmt = stmt.where(Review.comment.ilike(f"%{search}%"))
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, review_data: dict) -> Review:
        # Maybe we should use a procedure here?
        # Maybe not?
        # Maybe?

        review = self._create_via_procedure(review_data)
        self.db.commit()
        self.db.refresh(review)
        return review

    def update(self, review_id: int, review_data: dict) -> Review | None:
        obj = self.get(review_id)
        if not obj:
            return None
        for k, v in review_data.items():
            setattr(obj, k, v)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, review_id: int) -> bool:
        obj = self.get(review_id)
        if not obj:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True

    def _create_via_procedure(self, review_data: dict) -> Review:
        # Put your stored-proc call here.
        # If you paste your existing SQLReviewRepository.create_via_procedure implementation,
        # I can adapt it exactly.
        raise NotImplementedError
