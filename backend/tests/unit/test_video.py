import pytest
from pydantic import ValidationError

from app.schema.video_schema import VideoCreate


class TestVideoTitle:
    @pytest.mark.parametrize(
        "title",
        [
            "",
            "A" * 256,
            "A" * 257,
            "A" * 500,
            123,
            " ",
        ],
    )
    def test_invalid_title(self, title):
        with pytest.raises(ValidationError):
            VideoCreate(
                title=title,
                category="Test Category",
                link="https://test.com",
                game_id=1,
                language_id=1,
            )

    @pytest.mark.parametrize(
        "title",
        [
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "Top 10 Secrets You Won't Believe!",
            "Real-Time Gameplay Highlight",
        ],
    )
    def test_valid_title(self, title):
        video = VideoCreate(
            title=title,
            category="Test Category",
            link="https://test.com",
            game_id=1,
            language_id=1,
        )
        assert video.title == title


class TestVideoCategory:
    @pytest.mark.parametrize(
        "category",
        [
            "",
            "A" * 256,
            "A" * 257,
            "A" * 500,
            123,
            " ",
        ],
    )
    def test_invalid_category(self, category):
        with pytest.raises(ValidationError):
            VideoCreate(
                title="Test Title",
                category=category,
                link="https://test.com",
                game_id=1,
                language_id=1,
            )

    @pytest.mark.parametrize(
        "category",
        [
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "Magic / Fantasy Creatures",
            "Engine-Building",
        ],
    )
    def test_valid_category(self, category):
        video = VideoCreate(
            title="Test Title",
            category=category,
            link="https://test.com",
            game_id=1,
            language_id=1,
        )
        assert video.category == category


class TestVideoLink:
    @pytest.mark.parametrize(
        "link",
        [
            "",
            "A" * 256,
            "A" * 257,
            "A" * 500,
            123,
            " ",
        ],
    )
    def test_invalid_link(self, link):
        with pytest.raises(ValidationError):
            VideoCreate(
                title="Test Title",
                category="Test Category",
                link=link,
                game_id=1,
                language_id=1,
            )

    @pytest.mark.parametrize(
        "link",
        [
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "https://testsite.com",
            "https//fakeurl.com",
        ],
    )
    def test_valid_link(self, link):
        video = VideoCreate(
            title="Test Title",
            category="Test Category",
            link=link,
            game_id=1,
            language_id=1,
        )
        assert video.link == link
