from typing import List, Optional
import pandas as pd

from pydantic import BaseModel

class TagsBase(BaseModel):
    incident_id: str
    tag: str
class Tags(TagsBase):
    id: int

    class Config:
        orm_mode = True
class EvidenceBase(BaseModel):
    incident_id: str
    link: str

class Evidence(EvidenceBase):
    id: int

    class Config:
        orm_mode = True


class PlacesBase(BaseModel):
    city: str
    state_name: str
    state_code: str
    latitude: str
    longitude: str

class Places(PlacesBase):
    id: int
    
    class Config:
        orm_mode = True

class IncidentsBase(BaseModel):
    id: str
    place_id: int
    descr: str
    date: str

class Incidents(IncidentsBase):
    evidences: List[Evidence] = []
    tags: List[Tags] = []
    place: Places
    
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