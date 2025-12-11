import pytest
from pydantic import ValidationError

from app.schema.language_schema import LanguageCreate


class TestLanguage:
    @pytest.mark.parametrize(
        "language",
        [
            "",
            "A" * 256,
            "A" * 257,
            "A" * 500,
            123,
            " ",
        ],
    )
    def test_invalid_language(self, language):
        with pytest.raises(ValidationError):
            LanguageCreate(
                language=language,
            )

    @pytest.mark.parametrize(
        "language",
        [
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "Dansk!",
            "Swiss-German",
        ],
    )
    def test_valid_language(self, language):
        lang = LanguageCreate(
            language=language,
        )
        assert lang.language == language
