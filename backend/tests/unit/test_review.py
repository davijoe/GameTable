import pytest
from pydantic import ValidationError

from app.schema.review_schema import ReviewCreate


class TestReviewTitle:
    @pytest.mark.parametrize(
        "title",
        [
            "",
            "A" * 256,
            "A" * 257,
            "A" * 500,
            123,
        ],
    )
    def test_invalid_title(self, title):
        with pytest.raises(ValidationError):
            ReviewCreate(
                title=title,
                text=None,
                star_amount=5,
                user_id=1,
                game_id=1,
            )

    @pytest.mark.parametrize(
        "title",
        [
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "Best game ever!",
            "Worst-game-ever",
        ],
    )
    def test_valid_title(self, title):
        review = ReviewCreate(
            title=title,
            text=None,
            star_amount=5,
            user_id=1,
            game_id=1,
        )
        assert review.title == title


class TestReviewText:
    @pytest.mark.parametrize(
        "text",
        [
            "",
            "A" * 256,
            "A" * 257,
            "A" * 500,
            123,
        ],
    )
    def test_invalid_text(self, text):
        with pytest.raises(ValidationError):
            ReviewCreate(
                title="Test Review",
                text=text,
                star_amount=5,
                user_id=1,
                game_id=1,
            )

    @pytest.mark.parametrize(
        "text",
        [
            None,
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "The game is good because…",
            "Not bad - just ok",
        ],
    )
    def test_valid_text(self, text):
        review = ReviewCreate(
            title="Test Review",
            text=text,
            star_amount=5,
            user_id=1,
            game_id=1,
        )
        assert review.text == text


class TestReviewStarAmount:
    @pytest.mark.parametrize(
        "star_amount",
        [
            -5,
            -2,
            -1,
            0,
            11,
            12,
            15,
            "abc",
            5.5,
        ],
    )
    def test_invalid_star_amount(self, star_amount):
        with pytest.raises(ValidationError):
            ReviewCreate(
                title="Test Review",
                text=None,
                star_amount=star_amount,
                user_id=1,
                game_id=1,
            )

    @pytest.mark.parametrize(
        "star_amount",
        [
            1,
            2,
            5,
            9,
            10,
        ],
    )
    def test_valid_star_amount(self, star_amount):
        review = ReviewCreate(
            title="Test Review",
            text=None,
            star_amount=star_amount,
            user_id=1,
            game_id=1,
        )
        assert review.star_amount == star_amount

