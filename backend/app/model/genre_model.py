from sqlalchemy import Boolean, Column, Double, Integer, String, Text

from app.utility.db import Base


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    description = Column(String(255), nullable=True)
