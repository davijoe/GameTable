import pytest
from pydantic import ValidationError

from app.schema.artist_schema import ArtistCreate


class TestArtistName:
    @pytest.mark.parametrize(
        "name",
        [
            "",  # empty string
            "A" * 256,  # 256 characters (just over max)
            "A" * 257,  # 257 characters
            "A" * 500,  # 500 characters
            123,  # wrong data type
            " ",  # only space
            "-",  # only hyphens
        ],
    )
    def test_invalid_name(self, name):
        with pytest.raises(ValidationError):
            ArtistCreate(name=name)

    @pytest.mark.parametrize(
        "name",
        [
            "A",  # 1 character (minimum)
            "A" * 2,  # 2 characters
            "A" * 25,  # 25 characters (middle)
            "A" * 254,  # 254 characters
            "A" * 255,  # 255 characters (maximum)
            "Artist O'Neil",  # combining characters (apostrophe)
            "Artist-John",  # hyphen in name
        ],
    )
    def test_valid_name(self, name):
        """Test that valid name values are accepted."""
        artist = ArtistCreate(name=name)
        assert artist.name == name
