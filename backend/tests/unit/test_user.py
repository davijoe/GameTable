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


class TestUserDisplayName:
    @pytest.mark.parametrize(
        "display_name",
        [
            "",
            "A" * 26,
            "A" * 27,
            "A" * 40,
            123,
            " ",
        ],
    )
    def test_invalid_display_name(self, display_name):
        with pytest.raises(ValidationError):
            UserCreate(
                display_name=display_name,
                username="testuser",
                email="test@example.com",
                password="password123",
                dob=date(2000, 1, 1),
            )

    @pytest.mark.parametrize(
        "display_name",
        [
            "A",
            "A" * 2,
            "A" * 13,
            "A" * 24,
            "A" * 25,
            "John's",
            "Display-name",
        ],
    )
    def test_valid_display_name(self, display_name):
        user = UserCreate(
            display_name=display_name,
            username="testuser",
            email="test@example.com",
            password="password123",
            dob=date(2000, 1, 1),
        )
        assert user.display_name == display_name


class TestUserUsername:
    @pytest.mark.parametrize(
        "username",
        [
            "",
            "A" * 256,
            "A" * 257,
            "A" * 500,
            123,
            " ",
        ],
    )
    def test_invalid_username(self, username):
        with pytest.raises(ValidationError):
            UserCreate(
                display_name="Test",
                username=username,
                email="test@example.com",
                password="password123",
                dob=date(2000, 1, 1),
            )

    @pytest.mark.parametrize(
        "username",
        [
            "A",
            "A" * 2,
            "A" * 125,
            "A" * 254,
            "A" * 255,
            "Username’",
            "User-name",
        ],
    )
    def test_valid_username(self, username):
        user = UserCreate(
            display_name="Test",
            username=username,
            email="test@example.com",
            password="password123",
            dob=date(2000, 1, 1),
        )
        assert user.username == username


class TestUserPassword:
    @pytest.mark.parametrize(
        "password",
        [
            "P",
            "P" * 2,
            "P" * 3,
            "P" * 4,
            "P" * 5,
            "P" * 256,
            "P" * 257,
            "P" * 400,
            123,
            " ",
            "",
        ],
    )
    def test_invalid_password(self, password):
        with pytest.raises(ValidationError):
            UserCreate(
                display_name="Test",
                username="testuser",
                email="test@example.com",
                password=password,
                dob=date(2000, 1, 1),
            )

    @pytest.mark.parametrize(
        "password",
        [
            "P" * 6,
            "P" * 7,
            "P" * 125,
            "P" * 254,
            "P" * 255,
        ],
    )
    def test_valid_password(self, password):
        user = UserCreate(
            display_name="Test",
            username="testuser",
            email="test@example.com",
            password=password,
            dob=date(2000, 1, 1),
        )
        assert user.password == password


class TestUserEmail:
    @pytest.mark.parametrize(
        "email",
        [
            "user@" + "a" * 64 + ".com",
            "user@" + "a" * 65 + ".com",
            "user@" + "a" * 100 + ".com",
            "a" * 64 + "@" + "b" * 63 + "." + "c" * 63 + "." + "d" * 58 + ".com", #255 chars
            "a" * 64 + "@" + "b" * 63 + "." + "c" * 63 + "." + "d" * 59 + ".com", #256 chars
            "a" * 64 + "@" + "b" * 63 + "." + "c" * 63 + "." + "d" * 63 + "." + "e" * 63 + "." + "f" * 63 + "." + "g" * 11 + ".com", #400 chars
            "",
            " ",
            "us er@example.com",
            "example.com",
            "@example.com",
            "user@",
            123,
        ],
    )
    def test_invalid_email(self, email):
        with pytest.raises(ValidationError):
            UserCreate(
                display_name="Test",
                username="testuser",
                email=email,
                password="password123",
                dob=date(2000, 1, 1),
            )

    @pytest.mark.parametrize(
        "email",
        [
            "user@a.com",
            "user@" + "a" * 2 + ".com",
            "user@" + "a" * 30 + ".com",
            "user@" + "a" * 62 + ".com",
            "user@" + "a" * 63 + ".com",
            "a" * 64 + "@" + "b" * 63 + "." + "c" * 63 + "." + "d" * 56 + ".com", #253 chars
            "a" * 64 + "@" + "b" * 63 + "." + "c" * 63 + "." + "d" * 57 + ".com", #254 chars
        ],
    )
    def test_valid_email(self, email):
        user = UserCreate(
            display_name="Test",
            username="testuser",
            email=email,
            password="password123",
            dob=date(2000, 1, 1),
        )
        assert user.email == email
