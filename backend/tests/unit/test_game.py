import pytest
from pydantic import ValidationError

from app.schema.game_schema import GameCreate


class TestGameName:
    @pytest.mark.parametrize(
        "name",
        [
            "",  # empty string
            "A" * 256,  # 256 characters
            "A" * 257,  # 257 characters
            "A" * 500,  # 500 characters
            123,  # wrong data type
            " ",  # only space
            "-",  # only hyphens
        ],
    )
    def test_invalid_name(self, name):
        with pytest.raises(ValidationError):
            GameCreate(name=name)

    @pytest.mark.parametrize(
        "name",
        [
            "A",  # 1 character
            "A" * 2,  # 2 characters
            "A" * 25,  # 25 characters
            "A" * 254,  # 254 characters
            "A" * 255,  # 255 characters (max)
            "Formula Dé",  # combining characters
            "Ranter-Go-Round",  # hyphen
        ],
    )
    def test_valid_name(self, name):
        game = GameCreate(name=name)
        assert game.name == name


class TestGameSlug:
    @pytest.mark.parametrize(
        "slug",
        [
            "",  # empty string
            "A" * 256,  # 256 characters
            "A" * 257,  # 257 characters
            "A" * 500,  # 500 characters
            123,  # wrong data type
            " ",  # only space
            "-",  # only hyphens
        ],
    )
    def test_invalid_slug(self, slug):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", slug=slug)

    @pytest.mark.parametrize(
        "slug",
        [
            "a",  # 1 character
            "a" * 2,  # 2 characters
            "a" * 25,  # 25 characters
            "a" * 254,  # 254 characters
            "a" * 255,  # 255 characters (max)
            "game!",  # special characters
            "formula-dé",  # combining characters
        ],
    )
    def test_valid_slug(self, slug):
        game = GameCreate(name="Valid Name", slug=slug)
        assert game.slug == slug

    @pytest.mark.parametrize(
        "input_slug,expected_slug",
        [
            ("dragon quest", "dragon-quest"),  # spaces converted to hyphens
            ("Catan", "catan"),  # uppercase converted to lowercase
            ("Star Wars", "star-wars"),  # multiple conversions
        ],
    )
    def test_slug_normalization(self, input_slug, expected_slug):
        """Test that slug automatically normalizes spaces and uppercase."""
        game = GameCreate(name="Valid Name", slug=input_slug)
        assert game.slug == expected_slug
