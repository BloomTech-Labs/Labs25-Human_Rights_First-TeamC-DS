from sqlalchemy.orm import Session

from . import models, schemas

def create_incident(db: Session,  incident: schemas.Incidents):
    db_incident = models.Incidents(
        incident_id=incident.incident_id,
        incident_description=incident.incident_description,
        time_id=incident.time_id
        )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

def get_incident(db: Session, incident_id: str):
    return db.query(models.Incidents).filter(models.Incidents.incident_id == incident_id).first()

def get_incidents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Incidents).offset(skip).limit(limit).all()

def create_incident_evidence(db: Session, evidence: schemas.Evidence, incident_id: str):
    db_evidence = models.Evidences(**evidence.dict(), incident_id=incident_id)
    db.add(db_evidence)
    db.commit()
    db.refresh(db_evidence)
    return db_evidence

def get_evidences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Evidences).offset(skip).limit(limit).all()