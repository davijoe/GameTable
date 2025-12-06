from sqlalchemy import Column, Integer, String

from app.utility.db_sql import Base


class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True)
    language = Column(String(255), nullable=False)
