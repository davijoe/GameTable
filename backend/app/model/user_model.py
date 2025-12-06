from sqlalchemy import Column, Date, Integer, String

from app.utility.db_sql import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    display_name = Column(String(25), unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    dob = Column(Date, nullable=False)
    email = Column(String(255), nullable=False)
