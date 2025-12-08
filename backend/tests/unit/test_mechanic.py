import pytest
from pydantic import ValidationError

from app.schema.mechanic_schema import MechanicCreate


class TestMechanicName:
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
            MechanicCreate(name=name)

    @pytest.mark.parametrize(
        "name",
        [
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "Bingo!",
            "Deck-building",
        ],
    )
    def test_valid_name(self, name):
        mechanic = MechanicCreate(name=name)
        assert mechanic.name == name
