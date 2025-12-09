from datetime import date, timedelta

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


class TestArtistDob:
    @pytest.mark.parametrize(
        "dob",
        [
            date(1, 1, 1),
            date(1, 1, 2),
            date(1000, 6, 15),
            date(1899, 12, 30),
            date(1899, 12, 31),
            date.today() + timedelta(days=1), # small risk it could be valid if test runs at midnight
            date.today() + timedelta(days=2),
            date.today() + timedelta(days=60 * 365),
            "0000-00-00",
            "2000-00-05",
            "2005-03-00",
            "15-15-1990",
            "2000-13-10",
            "1980-04-31",
            "1900-02-29",
        ],
    )
    def test_invalid_dob(self, dob):
        with pytest.raises(ValidationError):
            ArtistCreate(name="Valid Name", dob=dob)

    @pytest.mark.parametrize(
        "dob",
        [
            date(1900, 1, 1),
            date(1900, 1, 2),
            date(1960, 12, 31),
            date.today() - timedelta(days=1),
            date.today(),
            "2000-02-29",
        ],
    )
    def test_valid_dob(self, dob):
        artist = ArtistCreate(name="Valid Name", dob=dob)
        expected = dob if isinstance(dob, date) else date.fromisoformat(dob)
        assert artist.dob == expected
