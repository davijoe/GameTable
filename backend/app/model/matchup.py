from sqlalchemy import Column, Integer, String, Double, Boolean, Text, Date
from app.utility.db import Base


class Matchup(Base):
    __tablename__ = "matchup"

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, nullable=False)
    start_time = Column(Date, nullable=True)
    end_time = Column(Date, nullable=True)
    created_at = Column(Date, nullable=True)
    is_private = Column(Boolean, nullable=False)
    created_by_user_id = Column(Integer, nullable=True)
    user_id_winner = Column(Integer, nullable=False)
    user_id_1 = Column(Integer, nullable=False)
    user_id_2 = Column(Integer, nullable=False)