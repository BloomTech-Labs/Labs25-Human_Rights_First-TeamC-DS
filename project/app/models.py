from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base

class Incidents(Base):
    __tablename__ = 'incidents'
    id = Column(String, primary_key=True)
    place_id = Column(String)
    edit_at = Column(String)
    text = Column(String)
    date = Column(String)

class Evidences(Base):
    __tablename__ = 'evidences'
    id = Column(Integer, primary_key=True)
    incident_id = Column(String)
    link_string = Column(String)

class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    state_code = Column(String)
    state_name = Column(String)
    county = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    counter = Column(Integer)

class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    incident_id = Column(String)
    tag = Column(Integer)

class TagsRef(Base):
    __tablename__ = 'tags_ref'
    id = Column(Integer, primary_key=True)
    tag = Column(String)