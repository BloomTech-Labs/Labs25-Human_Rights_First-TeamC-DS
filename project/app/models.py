from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Incidents(Base):
    __tablename__ = 'incidents'
    id = Column(String, primary_key=True)
    place_id = Column(Integer, ForeignKey('places.id'))
    descr = Column(String)
    date = Column(String)

    evidences = relationship('Evidences', foreign_keys='Evidences.incident_id')
    tags = relationship('Tags', primaryjoin="Incidents.id==Tags.incident_id")
    # places = relationship('Places', uselist=False, back_populates='incidents')

class Evidences(Base):
    __tablename__ = 'evidences'
    id = Column(Integer, primary_key=True)
    incident_id = Column(String, ForeignKey('incidents.id'))
    link = Column(String)


class Places(Base):
    __tablename__ = 'places'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    state_code = Column(String)
    state_name = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    counter = Column(Integer)
    # incidents = relationship("Incidents", back_populates="place_id")

class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    incident_id = Column(String, ForeignKey('incidents.id'))
    tag = Column(String)
    incident = relationship("Incidents", back_populates='tags')


class TagsRef(Base):
    __tablename__ = 'tags_ref'
    id = Column(Integer, primary_key=True)
    tag = Column(String)
