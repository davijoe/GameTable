from sqlalchemy import Column, Integer, String

from app.utility.db_sql import Base


class Genre(Base):
    __tablename__ = "genre"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    description = Column(String(255), nullable=True)
