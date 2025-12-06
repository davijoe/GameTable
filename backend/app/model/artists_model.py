from sqlalchemy import Column, Date, Integer, String

from app.utility.db_sql import Base


class Artists(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    dob = Column(Date, nullable=True)
