from typing import List

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import pandas as pd

from app.api import cron_update, predict, viz
from .database import SessionLocal, engine, get_db
from . import crud, models, schemas

tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=10000)

multilabel_binarizer = MultiLabelBinarizer()

models.Base.metadata.create_all(bind=engine)


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


app.include_router(cron_update.router)
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
