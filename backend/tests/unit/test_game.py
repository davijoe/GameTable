import pytest
from pydantic import ValidationError

from app.schema.game_schema import GameCreate


class TestGameName:
    @pytest.mark.parametrize(
        "name",
        [
            "",
            "A" * 256,
            "A" * 257,
            "A" * 500,
            123,
            " ",
            "-",
        ],
    )
    def test_invalid_name(self, name):
        with pytest.raises(ValidationError):
            GameCreate(name=name)

    @pytest.mark.parametrize(
        "name",
        [
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "Formula Dé",
            "Ranter-Go-Round",
        ],
    )
    def test_valid_name(self, name):
        game = GameCreate(name=name)
        assert game.name == name


class TestGameSlug:
    @pytest.mark.parametrize(
        "slug",
        [
            "",
            "A" * 256,
            "A" * 257,
            "A" * 500,
            123,
            " ",
            "-",
        ],
    )
    def test_invalid_slug(self, slug):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", slug=slug)

    @pytest.mark.parametrize(
        "slug",
        [
            "a",
            "a" * 2,
            "a" * 125,
            "a" * 254,
            "a" * 255,
            "game!",
            "formula-dé",
        ],
    )
    def test_valid_slug(self, slug):
        game = GameCreate(name="Valid Name", slug=slug)
        assert game.slug == slug

    @pytest.mark.parametrize(
        "input_slug,expected_slug",
        [
            ("dragon quest", "dragon-quest"),
            ("Catan", "catan"),
            ("Star Wars", "star-wars"),
        ],
    )
    def test_slug_normalization(self, input_slug, expected_slug):
        game = GameCreate(name="Valid Name", slug=input_slug)
        assert game.slug == expected_slug


class TestGameYearPublished:
    @pytest.mark.parametrize(
        "year_published",
        [
            -1000,
            -2,
            -1,
            0,
            1,
            2,
            1000,
            1899,
            1900,
            2156,
            2157,
            2500,
            "abc",
            1999.5,
        ],
    )
    def test_invalid_year_published(self, year_published):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", year_published=year_published)

    @pytest.mark.parametrize(
        "year_published",
        [
            1901,
            1902,
            2000,
            2154,
            2155,
        ],
    )
    def test_valid_year_published(self, year_published):
        game = GameCreate(name="Valid Name", year_published=year_published)
        assert game.year_published == year_published


class TestGameBggRating:
    @pytest.mark.parametrize(
        "bgg_rating",
        [
            -5,
            -0.02,
            -0.01,
            0,
            0.01,
            0.02,
            0.5,
            0.98,
            0.99,
            10.01,
            10.02,
            15,
            "abc",
            -1,
            5.1234,
        ],
    )
    def test_invalid_bgg_rating(self, bgg_rating):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", bgg_rating=bgg_rating)

    @pytest.mark.parametrize(
        "bgg_rating",
        [
            1,
            1.01,
            5,
            9.99,
            10,
        ],
    )
    def test_valid_bgg_rating(self, bgg_rating):
        game = GameCreate(name="Valid Name", bgg_rating=bgg_rating)
        assert game.bgg_rating == bgg_rating


class TestGameDifficultyRating:
    @pytest.mark.parametrize(
        "difficulty_rating",
        [
            -2.5,
            -0.02,
            -0.01,
            0,
            0.01,
            0.02,
            0.5,
            0.98,
            0.99,
            5.01,
            5.02,
            7.5,
            "abc",
            -1,
            5.1234,
        ],
    )
    def test_invalid_difficulty_rating(self, difficulty_rating):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", difficulty_rating=difficulty_rating)

    @pytest.mark.parametrize(
        "difficulty_rating",
        [
            1,
            1.01,
            2.5,
            4.99,
            5,
        ],
    )
    def test_valid_difficulty_rating(self, difficulty_rating):
        game = GameCreate(name="Valid Name", difficulty_rating=difficulty_rating)
        assert game.difficulty_rating == difficulty_rating


MAX_BYTES = 65535


class TestGameDescription:
    @pytest.mark.parametrize(
        "param",
        [
            {"type": "value", "value": ""},
            {
                "type": "length",
                "value": MAX_BYTES + 1,
            },
            {
                "type": "length",
                "value": MAX_BYTES + 2,
            },
            {"type": "length", "value": MAX_BYTES + 10000},
        ],
    )
    def test_invalid_descriptions(self, param):
        if param["type"] == "value":
            desc = param["value"]
        else:
            desc = "A" * param["value"]

        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", description=desc)

    @pytest.mark.parametrize(
        "param",
        [
            {"type": "value", "value": "0"},
            {"type": "length", "value": 1},
            {"type": "length", "value": 2},
            {"type": "length", "value": int(MAX_BYTES / 2)},
            {"type": "length", "value": MAX_BYTES - 1},
            {"type": "length", "value": MAX_BYTES - 2},
            {"type": "length", "value": MAX_BYTES},
        ],
    )
    def test_valid_descriptions(self, param):
        if param["type"] == "value":
            desc = param["value"]
        else:
            desc = "A" * param["value"]
        game = GameCreate(name="Valid Name", description=desc)
        assert game.description == desc


class TestGameMinPlayers:
    @pytest.mark.parametrize(
        "min_players",
        [
            -500,
            -2,
            -1,
            0,
            1000,
            1001,
            1500,
            "abc",
            5.5,
        ],
    )
    def test_invalid_min_players(self, min_players):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", min_players=min_players)

    @pytest.mark.parametrize(
        "min_players",
        [
            1,
            2,
            500,
            998,
            999,
        ],
    )
    def test_valid_min_players(self, min_players):
        game = GameCreate(name="Valid Name", min_players=min_players)
        assert game.min_players == min_players


class TestGameMaxPlayers:
    @pytest.mark.parametrize(
        "max_players",
        [
            -500,
            -2,
            -1,
            0,
            1000,
            1001,
            1500,
            "abc",
            5.5,
        ],
    )
    def test_invalid_max_players(self, max_players):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", max_players=max_players)

    @pytest.mark.parametrize(
        "max_players",
        [
            1,
            2,
            500,
            998,
            999,
        ],
    )
    def test_valid_max_players(self, max_players):
        game = GameCreate(name="Valid Name", max_players=max_players)
        assert game.max_players == max_players
        assert game.max_players == max_players


class TestGameThumbnail:
    @pytest.mark.parametrize(
        "thumbnail",
        [
            "",
            "A" * 1025,
            "A" * 1026,
            "A" * 1500,
            123,
            " ",
            "https://example.com/user profile",
        ],
    )
    def test_invalid_thumbnail(self, thumbnail):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", thumbnail=thumbnail)

    @pytest.mark.parametrize(
        "thumbnail",
        [
            "A",
            "A" * 2,
            "A" * 500,
            "A" * 1023,
            "A" * 1024,
            "https://cf.geekdo-images.com/rpwCZAjYLD940NWwP3SRoA__small/img/YT6svCVsWqLrDitcMEtyazVktbQ=/fit-in/200x150/filters:strip_icc()/pic4718279.jpg",
        ],
    )
    def test_valid_thumbnail(self, thumbnail):
        game = GameCreate(name="Valid Name", thumbnail=thumbnail)
        assert game.thumbnail == thumbnail


class TestGameImage:
    @pytest.mark.parametrize(
        "image",
        [
            "",
            "A" * 1025,
            "A" * 1026,
            "A" * 1500,
            123,
            " ",
            "https://example.com/user profile",
        ],
    )
    def test_invalid_image(self, image):
        with pytest.raises(ValidationError):
            GameCreate(name="Valid Name", image=image)

    @pytest.mark.parametrize(
        "image",
        [
            "A",
            "A" * 2,
            "A" * 500,
            "A" * 1023,
            "A" * 1024,
            "https://cf.geekdo-images.com/rpwCZAjYLD940NWwP3SRoA__original/img/yR0aoBVKNrAmmCuBeSzQnMflLYg=/0x0/filters:format(jpeg)/pic4718279.jpg",
        ],
    )
    def test_valid_image(self, image):
        game = GameCreate(name="Valid Name", image=image)
        assert game.image == image
