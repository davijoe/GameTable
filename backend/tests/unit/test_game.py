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


class TestGameYearPublished:
    @pytest.mark.parametrize(
        "year_published",
        [
            0,  # zero (invalid)
            1,  # 0001
            2,  # 0002
            1500,  # before 1901
            1899,  # before 1901
            1900,  # boundary before 1901
            2156,  # after 2155
            2157,  # after 2155
            2500,  # after 2155
            "abc",  # wrong data type
            12345,  # more than 4 digits
            1999.5,  # decimal value
            99,  # two-digit year
        ],
    )
    def test_invalid_year_published(self, year_published):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", year_published=year_published)

    @pytest.mark.parametrize(
        "year_published",
        [
            1901,  # boundary: earliest valid
            1902,  # just after boundary
            2000,  # mid-range valid
            2154,  # just before upper boundary
            2155,  # boundary: latest valid
        ],
    )
    def test_valid_year_published(self, year_published):
        game = GameCreate(name="Valid Name", year_published=year_published)
        assert game.year_published == year_published


class TestGameBggRating:
    @pytest.mark.parametrize(
        "bgg_rating",
        [
            0,  # 0
            0.01,  # 0.01
            0.5,  # 0.5
            0.98,  # 0.98
            0.99,  # 0.99
            10.01,  # 10.01
            10.02,  # 10.02
            15,  # 15
            "abc",  # wrong data type
            -1,  # negative value
            5.1234,  # too many decimals
        ],
    )
    def test_invalid_bgg_rating(self, bgg_rating):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", bgg_rating=bgg_rating)

    @pytest.mark.parametrize(
        "bgg_rating",
        [
            1,  # boundary: lowest valid
            1.01,  # just above boundary
            5,  # mid-range valid
            9.99,  # just below upper boundary
            10,  # boundary: highest valid
        ],
    )
    def test_valid_bgg_rating(self, bgg_rating):
        game = GameCreate(name="Valid Name", bgg_rating=bgg_rating)
        assert game.bgg_rating == bgg_rating


class TestGameDifficultyRating:
    @pytest.mark.parametrize(
        "difficulty_rating",
        [
            0,  # 0
            0.01,  # 0.01
            0.5,  # 0.5
            0.98,  # 0.98
            0.99,  # 0.99
            5.01,  # 5.01
            5.02,  # 5.02
            7.5,  # 7.5
            "abc",  # wrong data type
            -1,  # negative value
            5.1234,  # too many decimals
        ],
    )
    def test_invalid_difficulty_rating(self, difficulty_rating):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", difficulty_rating=difficulty_rating)

    @pytest.mark.parametrize(
        "difficulty_rating",
        [
            1,  # boundary: lowest valid
            1.01,  # just above boundary
            2.5,  # mid-range valid
            4.99,  # just below upper boundary
            5,  # boundary: highest valid
        ],
    )
    def test_valid_difficulty_rating(self, difficulty_rating):
        game = GameCreate(name="Valid Name", difficulty_rating=difficulty_rating)
        assert game.difficulty_rating == difficulty_rating


class TestGameMinPlayers:
    @pytest.mark.parametrize(
        "min_players",
        [
            0,  # less than 1
            -1,  # negative value
            1000,  # 1000 (exceeds max)
            1001,  # 1001 (exceeds max)
            1500,  # 1500 (exceeds max)
            "abc",  # wrong data type
            5.5,  # decimal
        ],
    )
    def test_invalid_min_players(self, min_players):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", min_players=min_players)

    @pytest.mark.parametrize(
        "min_players",
        [
            1,  # boundary: lowest valid
            2,  # just above boundary
            500,  # mid-range valid
            998,  # just below upper boundary
            999,  # boundary: highest valid
        ],
    )
    def test_valid_min_players(self, min_players):
        game = GameCreate(name="Valid Name", min_players=min_players)
        assert game.min_players == min_players


class TestGameMaxPlayers:
    @pytest.mark.parametrize(
        "max_players",
        [
            0,  # less than 1
            -1,  # negative value
            1000,  # 1000 (exceeds max)
            1001,  # 1001 (exceeds max)
            1500,  # 1500 (exceeds max)
            "abc",  # wrong data type
            5.5,  # decimal
        ],
    )
    def test_invalid_max_players(self, max_players):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", max_players=max_players)

    @pytest.mark.parametrize(
        "max_players",
        [
            1,  # boundary: lowest valid
            2,  # just above boundary
            500,  # mid-range valid
            998,  # just below upper boundary
            999,  # boundary: highest valid
        ],
    )
    def test_valid_max_players(self, max_players):
        game = GameCreate(name="Valid Name", max_players=max_players)
        assert game.max_players == max_players
