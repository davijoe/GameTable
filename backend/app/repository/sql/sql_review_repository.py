from typing import List  # noqa: UP035 # disable warning because of current python ver

from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.model.review_model import Review


class SQLReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, review_id: int) -> Review | None:
        return self.db.get(Review, review_id)

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[Review], int]:
        stmt = select(Review)
        if search:
            like = f"%{search}%"
            stmt = stmt.where(Review.title.ilike(like))
        total = self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create(self, review: Review) -> Review:
        self.db.add(review)
        self.db.flush()
        return review

    def update(self, review: Review) -> Review:
        self.db.merge(review)
        self.db.flush()
        return review

    def delete(self, review: Review) -> None:
        self.db.delete(review)
        self.db.flush()

    def get_review_count_for_game(self, game_id: int) -> int:
        stmt = text("SELECT GetGameReviewCount(:game_id)")
        result = self.db.execute(stmt, {"game_id": game_id}).scalar_one()
        return result

    def list_by_game(self, game_id: int) -> List[Review]:  # noqa: UP006 # disable warning because of current python ver
        stmt = select(Review).where(Review.game_id == game_id)
        return self.db.execute(stmt).scalars().all()

