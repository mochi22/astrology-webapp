from sqlalchemy import Column, Integer, String
from src.database import Base

class Punishment(Base):
    __tablename__ = "punishments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    category = Column(String, nullable=False)
    likes = Column(Integer, default=0)