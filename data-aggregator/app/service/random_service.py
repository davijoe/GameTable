from datetime import date, timedelta
import random


def random_dob() -> date:
    today = date.today()
    min_age = 18
    max_age = 75

    age = random.randint(min_age, max_age)
    days_offset = random.randint(0, 364)
    return today.replace(year=today.year - age) - timedelta(days=days_offset)


EMAIL_HOSTS = [
    "gmail.com",
    "hotmail.com",
    "outlook.com",
    "yahoo.com",
    "protonmail.com",
    "aol.com",
    "icloud.com",
]


def random_email_for(username: str) -> str:
    host = random.choice(EMAIL_HOSTS)
    return f"{username}@{host}"
