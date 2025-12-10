from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.orm import relationship

from app.utility.db_sql import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    display_name = Column(String(55), unique=True, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    dob = Column(Date, nullable=False)
    email = Column(String(255), nullable=False)

    is_admin = Column(Boolean, default=False)

    reviews = relationship("Review", lazy="select")
