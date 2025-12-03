from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String(55), nullable=False, unique=True, index=True)
    username = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    # one-to-many: a user can have many reviews
    reviews = relationship(
        "Review",
        back_populates="user",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r}>"
