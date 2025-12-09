import pytest
from pydantic import ValidationError

from app.schema.genre_schema import GenreCreate


class TestGenreName:
    @pytest.mark.parametrize(
        "name",
        [
            "",
            "A" * 31,
            "A" * 32,
            "A" * 45,
            123,
            " ",
            "-",
        ],
    )
    def test_invalid_name(self, name):
        with pytest.raises(ValidationError):
            GenreCreate(name=name)

    @pytest.mark.parametrize(
        "name",
        [
            "A",
            "A" * 2,
            "A" * 15,
            "A" * 29,
            "A" * 30,
            "Children's",
            "Euro-style",
        ],
    )
    def test_valid_name(self, name):
        genre = GenreCreate(name=name)
        assert genre.name == name
