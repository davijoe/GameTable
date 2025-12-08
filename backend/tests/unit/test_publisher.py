import pytest
from pydantic import ValidationError

from app.schema.publisher_schema import PublisherCreate


class TestPublisherName:
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
            PublisherCreate(name=name)

    @pytest.mark.parametrize(
        "name",
        [
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "Publisher O'Neil",
            "Publisher-John",
        ],
    )
    def test_valid_name(self, name):
        publisher = PublisherCreate(name=name)
        assert publisher.name == name
