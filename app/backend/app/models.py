from sqlalchemy import Column, Integer, Text, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(JSON)
    tags = Column(JSON)
