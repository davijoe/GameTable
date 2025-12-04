from sqlalchemy import Boolean, Column, Date, Double, Integer, String, Text

from app.utility.db import Base


class Designer(Base):
    __tablename__ = "designer"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    dob = Column(Date, nullable=True)
