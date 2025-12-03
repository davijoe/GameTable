from sqlalchemy import Column, Integer, String

from app.utility.db import Base


class Mechanic(Base):
    __tablename__ = "mechanic"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    