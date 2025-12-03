from sqlalchemy.orm import Session

import bcrypt

from app.model.user_model import User
from app.service.random_service import random_dob, random_email_for


def get_or_create_bgg_user(db: Session, username: str) -> User:
    user = db.query(User).filter_by(username=username).one_or_none()
    if user is not None:
        return user

    display_name = username[:55]
    raw_password = username.encode("utf-8")
    hashed = bcrypt.hashpw(raw_password, bcrypt.gensalt()).decode("utf-8")

    user = User(
        display_name=display_name,
        username=username,
        password=hashed,
        dob=random_dob(),
        email=random_email_for(username),
    )
    db.add(user)
    db.flush()
    return user
