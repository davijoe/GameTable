import pytest
from pydantic import ValidationError

from app.schema.designer_schema import DesignerCreate


class TestDesignerName:
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
            DesignerCreate(name=name)

    @pytest.mark.parametrize(
        "name",
        [
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "Designer O'Neil",
            "Designer-John",
        ],
    )
    def test_valid_name(self, name):
        designer = DesignerCreate(name=name)
        assert designer.name == name
