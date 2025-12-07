import pytest
from pydantic import ValidationError

from app.schema.genre_schema import GenreCreate


class TestGenreName:
    @pytest.mark.parametrize(
        "name",
        [
            "",  # empty string
            "A" * 31,  # 31 characters (just over max)
            "A" * 32,  # 32 characters
            "A" * 45,  # 45 characters
            123,  # wrong data type
            " ",  # only space
            "-",  # only hyphens
        ],
    )
    def test_invalid_name(self, name):
        with pytest.raises(ValidationError):
            GenreCreate(name=name)

    @pytest.mark.parametrize(
        "name",
        [
            "A",  # 1 character (minimum)
            "A" * 2,  # 2 characters
            "A" * 15,  # 15 characters (middle)
            "A" * 29,  # 29 characters
            "A" * 30,  # 30 characters (maximum)
            "Children's",  # combining characters (apostrophe)
            "Euro-style",  # hyphen in name
        ],
    )
    def test_valid_name(self, name):
        genre = GenreCreate(name=name)
        assert genre.name == name
