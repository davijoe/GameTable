import pytest
from pydantic import ValidationError

from app.schema.artist_schema import ArtistCreate


class TestArtistName:
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
            ArtistCreate(name=name)

    @pytest.mark.parametrize(
        "name",
        [
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "Artist O'Neil",
            "Artist-John",
        ],
    )
    def test_valid_name(self, name):
        artist = ArtistCreate(name=name)
        assert artist.name == name
