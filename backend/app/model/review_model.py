from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.utility.db_sql import Base


class Review(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    text = Column(String(255), nullable=True)
    star_amount = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    game_id = Column(Integer, ForeignKey("game.id"), nullable=False)

    user = relationship("User", back_populates="reviews", lazy="joined")
