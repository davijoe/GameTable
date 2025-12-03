from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base

from app.model.game_model import game_reviews


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    text = Column(String(255), nullable=True)
    star_amount = Column(Integer, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="reviews",
    )

    games = relationship(
        "Game",
        secondary=game_reviews,
        back_populates="reviews",
    )

    def __repr__(self) -> str:
        return f"<Review id={self.id} user_id={self.user_id} star_amount={self.star_amount}>"
