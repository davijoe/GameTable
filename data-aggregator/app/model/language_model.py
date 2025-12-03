from sqlalchemy import Column, Integer, String

from .base import Base


class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True, index=True)
    language = Column(String(255), nullable=False, unique=True)
