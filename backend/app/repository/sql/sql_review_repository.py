from typing import List  # noqa: UP035 # disable warning because of current python ver

from sqlalchemy import func, select, text
from sqlalchemy.orm import Session

from app.model.review_model import Review
from app.schema.review_schema import ReviewCreate, ReviewRead


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
        self.db.commit()
        return review

    def update(self, review: Review) -> Review:
        self.db.merge(review)
        self.db.commit()
        return review

    def delete(self, review: Review) -> None:
        self.db.delete(review)
        self.db.commit()

    def get_review_count_for_game(self, game_id: int) -> int:
        stmt = text("SELECT GetGameReviewCount(:game_id)")
        result = self.db.execute(stmt, {"game_id": game_id}).scalar_one()
        return result

    def list_by_game(self, game_id: int, offset: int = 0, limit: int = 5):
        stmt = select(Review).where(Review.game_id == game_id)
        total = self.db.execute(select(func.count()).select_from(stmt.subquery())).scalar_one()
        rows = self.db.execute(stmt.offset(offset).limit(limit)).scalars().all()
        return rows, total

    def create_via_procedure(self, payload: ReviewCreate) -> Review:
        stmt = text("""
            CALL add_game_review(
                :p_user_id,
                :p_game_id,
                :p_title,
                :p_text,
                :p_stars
            )
        """)
        params = {
            "p_user_id": payload.user_id,
            "p_game_id": payload.game_id,
            "p_title": payload.title,
            "p_text": payload.text,
            "p_stars": payload.star_amount,
        }
        result = self.db.execute(stmt, params)
        new_id = result.fetchone()[0] # fetch the id from newly made review
        return self.db.get(Review, new_id)
