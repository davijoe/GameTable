import pytest
from pydantic import ValidationError

from app.schema.mechanic_schema import MechanicCreate


class TestMechanicName:
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
            MechanicCreate(name=name)

    @pytest.mark.parametrize(
        "name",
        [
            "A",  # 1 character (minimum)
            "A" * 2,  # 2 characters
            "A" * 25,  # 25 characters (middle)
            "A" * 254,  # 254 characters
            "A" * 255,  # 255 characters (maximum)
            "Bingo!",  # combining characters / punctuation
            "Deck-building",  # hyphen in name
        ],
    )
    def test_valid_name(self, name):
        """Test that valid name values are accepted."""
        mechanic = MechanicCreate(name=name)
        assert mechanic.name == name
