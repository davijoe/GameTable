from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from app.schema.user_schema import UserCreate


class TestUserDob:
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
            UserCreate(
                display_name="Test",
                username="testuser",
                email="test@example.com",
                password="password123",
                dob=dob,
            )

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
        user = UserCreate(
            display_name="Test",
            username="testuser",
            email="test@example.com",
            password="password123",
            dob=dob,
        )
        expected = dob if isinstance(dob, date) else date.fromisoformat(dob)
        assert user.dob == expected
