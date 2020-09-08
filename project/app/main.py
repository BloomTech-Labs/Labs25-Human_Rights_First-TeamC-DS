from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api import predict, viz
from sqlalchemy.orm import Session
from .database import SessionLocal, engine

from . import crud, models, schemas

from typing import List

import pickle
import pandas as pd

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


@app.get("/incidents/", response_model=List[schemas.Incidents])
def read_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    incidents = crud.get_incidents(db, skip=skip, limit=limit)
    return incidents


@app.post('/cron_update/', response_model=List[schemas.PBIncidents])
def read_pbincidents(pbincidents: list):
    df = pd.DataFrame(pbincidents)


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
