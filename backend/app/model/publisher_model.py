from sqlalchemy import Column, Integer, String

from app.utility.db import Base


class Publisher(Base):
    __tablename__ = "publisher"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    