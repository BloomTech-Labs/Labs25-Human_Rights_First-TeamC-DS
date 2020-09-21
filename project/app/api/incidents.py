from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import SessionLocal, engine, get_db
from .. import crud, models, schemas

router = APIRouter()

@router.get("/incidents/", response_model=List[schemas.Incidents])
def read_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    incidents = crud.get_incidents(db, skip=skip, limit=limit)
    return incidents

@router.get("/incidents/{tag}", response_model=List[schemas.Incidents])
def incidents_by_tag(tag: str, db: Session = Depends(get_db)):
    # query 'tags' table filter by tags.tag == tag
    list_of_ids = db.query(models.Tags.incident_id).filter(models.Tags.tag == tag.capitalize()).all()
    tag_incidents = []
    for incident_id in list_of_ids:
        incident = crud.get_incident(db,incident_id)
        tag_incidents.append(incident)
    return tag_incidents
