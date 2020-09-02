from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base

class Incidents(Base):
    __tablename__ = 'incidents'
    id = Column(Integer, primary_key=True)
    incident_id = Column(String)
    incident_description = Column(String)
    time_id = Column(String)

    evidences = relationship('Evidences', back_populates='incident')
    place = relationship('Place', back_populates='incident')

class Evidences(Base):
    __tablename__ = 'evidences'
    id = Column(Integer, primary_key=True)
    link_string = Column(String)
    incident_id = Column(String, ForeignKey('incidents.incident_id'))

    incident = relationship('Incidents', back_populates="evidences")

class Place(Base):
    __tablename__ = 'place'
    id = Column(Integer, primary_key=True)
    incident_id = Column(String, ForeignKey('incidents.incident_id'))
    city = Column(String)
    state = Column(String)
    state_code = Column(String)
    latitude = Column(String)
    longitude = Column(String)

    incident = relationship('Incidents', back_populates='place')

class TagsJunction(Base):
    __tablename__ = 'tagsjunction'
    id = Column(Integer, primary_key=True)
    incident_id = Column(String, ForeignKey('incidents.incident_id'))
    force_tag_id = Column(Integer, ForeignKey('forcetags.force_id'))

class ForceTags(Base):
    __tablename__ = 'forcetags'
    id = Column(Integer, primary_key=True)
    force_id = Column(Integer, ForeignKey('tagsjunction.force_tag_id'))
    force_string = Column(String)