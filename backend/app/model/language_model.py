from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.utility.db_sql import Base


class Language(Base):
    __tablename__ = "language"

    id = Column(Integer, primary_key=True)
    language = Column(String(255), nullable=False)

    videos = relationship("Video", lazy="select")
