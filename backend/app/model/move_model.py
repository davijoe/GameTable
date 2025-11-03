from sqlalchemy import Column, Integer, String, Double, Boolean, Text
from app.utility.db import Base


class Move(Base):
    __tablename__ = "move"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ply = Column(Integer, nullable=False)
    start_x_coordinate = Column(Integer, nullable=False)
    start_y_coordinate = Column(Integer, nullable=False)
    end_x_coordinate = Column(Integer, nullable=True)
    end_y_coordinate = Column(Integer, nullable=True)