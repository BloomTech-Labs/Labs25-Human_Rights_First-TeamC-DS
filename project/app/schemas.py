from typing import List, Optional
import pandas as pd

from pydantic import BaseModel

class EvidenceBase(BaseModel):
    link_string: str

class Evidence(EvidenceBase):
    id: int

    class Config:
        orm_mode = True


class PlaceBase(BaseModel):
    city: str
    state: str
    state_code: str
    latitude: str
    longitude: str

class Place(PlaceBase):
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
    place: List[Place] = []
    
    class Config:
        orm_mode = True

class PBIncident(BaseModel):
    """ Use this data model to parse the request body JSON."""
    # ['links', 'state', 'edit_at', 'city', 'name', 'date', 'date_text', 'id']
    links: List[str]
    state: str
    edit_at: str
    city: str
    name: str
    date: str
    date_text: str
    id: str