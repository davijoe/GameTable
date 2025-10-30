from sqlalchemy import Column, Integer, String, Double, Boolean, Text, Date
from app.utility.db import Base


class Artists(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    dob = Column(Date, nullable=True)