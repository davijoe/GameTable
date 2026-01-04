from app.repository.review.review_repository_factory import get_review_repository
from app.schema.review_schema import ReviewCreate, ReviewRead, ReviewUpdate


class ReviewService:
    def __init__(self):
        self.repo = get_review_repository()

    def get(self, review_id: int) -> ReviewRead | None:
        obj = self.repo.get(review_id)
        return ReviewRead.model_validate(obj) if obj else None

    def get_review_count_for_game(self, game_id: int) -> int:
        return self.repo.get_review_count_for_game(game_id)

    def list_by_game(
        self, game_id: int, offset: int = 0, limit: int = 5
    ) -> tuple[list[ReviewRead], int]:
        rows, total = self.repo.list_by_game(game_id, offset, limit)
        return [ReviewRead.model_validate(r) for r in rows], total

    def list(
        self, offset: int = 0, limit: int = 50, search: str | None = None
    ) -> tuple[list[ReviewRead], int]:
        rows, total = self.repo.list(offset, limit, search)
        return [ReviewRead.model_validate(r) for r in rows], total

    def create(self, payload: ReviewCreate) -> ReviewRead:
        # review = self.repo.create_via_procedure(payload)  # uses stored procedure
        # Perhaps use again?
        obj = self.repo.create(payload.model_dump())
        return ReviewRead.model_validate(obj)

    def update(self, review_id: int, payload: ReviewUpdate) -> ReviewRead | None:
        obj = self.repo.update(
            review_id,
            payload.model_dump(exclude_unset=True),
        )
        return ReviewRead.model_validate(obj) if obj else None

    def delete(self, review_id: int) -> bool:
        obj = self.repo.delete(review_id)
        if not obj:
            return False
        return True
