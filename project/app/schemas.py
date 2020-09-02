from typing import List, Optional

from pydantic import BaseModel

class EvidenceBase(BaseModel):
    link_string: str

class Evidence(EvidenceBase):
    id: int

    class Config:
        orm_mode = True

class IncidentsBase(BaseModel):
    incident_id: str
    incident_description: str
    time_id: str

class Incidents(IncidentsBase):
    id: int
    evidences: List[Evidence] = []
    
    class Config:
        orm_mode = True

class PlaceBase(BaseModel):
    city: str
    state: str
    state_code: str
    latitude: int
    longitude: int

class Place(PlaceBase):
    id: int
    
    class Config:
        orm_mode = True

# class Place(Base):
#     __tablename__ = 'place'
#     id = Column(Integer, primary_key=True)
#     incident_id = Column(String, ForeignKey('incidents.incident_id'))
#     city = Column(String)
#     state = Column(String)
#     state_code = Column(String)
#     latitude = Column(Integer)
#     longitude = Column(Integer)

#     incident = relationship('Incidents', back_populates='place')

# class Tags_Junction(Base):
#     __tablename__ = 'tags_junction'
#     id = Column(Integer, primary_key=True)
#     incident_id = Column(String, ForeignKey('incidents.incident_id'))
#     force_tag_id = Column(Integer, ForeignKey('forcetags.force_id'))

# class ForceTags(Base):
#     __tablename__ = 'forcetags'
#     id = Column(Integer, primary_key=True)
#     force_id = Column(Integer, ForeignKey('tags_junction.force_tag_id'))
#     force_string = Column(String)