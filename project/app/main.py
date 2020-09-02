from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import predict, viz
from sqlalchemy.orm import Session
from .database import SessionLocal, engine

from . import crud, models, schemas

from typing import List

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title='Human-Rights-first-Police-Tracker DS API',
    description='Search locations where use of police force is reported on social media',
    version='0.1',
    docs_url='/',
)

@app.post("/incidents/", response_model=schemas.Incidents)
def create_incident(incident: schemas.Incidents, db: Session = Depends(get_db)):
    db_incident = crud.get_incident(db, incident_id=incident.incident_id)
    if db_incident:
        raise HTTPException(status_code=400, detail='incident already exists')
    return crud.create_incident(db=db, incident=incident)

@app.get("/incidents/", response_model=List[schemas.Incidents])
def read_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    incidents = crud.get_incidents(db, skip=skip,limit=limit)
    return incidents

@app.post('/incidents/{incident_id}/evidence/', response_model=schemas.Evidence)
def create_evidence_for_incident(incident_id: str, evidence: schemas.Evidence, db: Session = Depends(get_db)):
    return crud.create_incident_evidence(db, evidence=evidence, incident_id=incident_id)

@app.get('/evidences/', response_model=List[schemas.Evidence])
def read_evidences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    evidences = crud.get_evidences(db, skip=skip, limit=limit)
    return evidences

app.include_router(predict.router)
app.include_router(viz.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
