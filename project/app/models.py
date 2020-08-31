from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Evidence(Base):
    __tablename__ = 'evidence'
    id = Column(Integer, primary_key=True)