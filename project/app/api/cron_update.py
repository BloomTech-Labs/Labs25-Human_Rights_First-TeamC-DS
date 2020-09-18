from typing import List
import pickle

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd

from ..database import SessionLocal, engine, get_db
from .. import crud, models, schemas
from ..utilities import get_new, clean_pb2020, geoloc

router = APIRouter()
# con = engine.connect()


@router.post('/cron_update/')
def read_pbincidents(pbincident: List[schemas.PBIncident], db: Session = Depends(get_db)):
    # list incidents into dicts to create dataframe
    list_incidents = [i.dict() for i in pbincident]
    df = pd.DataFrame.from_dict(list_incidents, orient='columns')

    counts = crud.get_places(db)
    city_counts = {i[1]: {i[0]: i[2]} for i in counts}

    allnew_idcount = []
    for i in list(df['id']):
        id_split = i.split('-')
        city = id_split[1].capitalize()
        state = id_split[0].upper()
        if int(id_split[-1]) > city_counts[state][city]:
            allnew_idcount.append(i)

    updates_df = df[df['id'].isin(allnew_idcount)].copy()

    # clean functions
    # get new incidents
    df = get_new(df)

    # clean new incidents
    df = clean_pb2020(df)

    # add locaiton metadata to incidents
    df = geoloc(df)

    # this is the code for the second pickle
    # Load from file
    with open('app/vect_bin_pickle.pkl', 'rb') as file:
        picklefile = pickle.load(file)
    # take the new data and vectorize it for the model
    # run vectorized data through model
    tfidf_vectorizer = picklefile['tfidf']
    df_tfidf = tfidf_vectorizer.transform(df['text'])

    clf2 = picklefile['clf']
    y_pred = clf2.predict(df_tfidf)
    # get predictions and inverse transform the results so we can read the results
    multilabel_binarizer = picklefile['mlb']
    df['tag_predicted'] = multilabel_binarizer.inverse_transform(y_pred)
    # clean the results by eliminating commas and parenthesis, append to df
    df['tag_predicted'] = df['tag_predicted'].apply(lambda x: ', '.join(x))
    print(df.columns)

    # Separates the tags by category into different rows
    df = df.explode('tag_predicted')
    # use db to query
    # row by row check if exists in db
    # check id column

    # TODO chunk this into another fxn (?)
    # INSERT INTO incident_dim
    # (incident_id, text, edit_at, date, city)
    inicident_df = df[['id', 'text', 'edit_at', 'date', 'CITY']].copy()
    inicident_df.to_sql('incident_dim', con,
                        if_exists='append', index=False, method='multi')
    print(inicident_df.columns)
    # INSERT INTO place_dim
    # (incident_id, city, state_code, state_name, county, latitude, longitude)
    # place_df = df[['id', 'city', 'state_code', 'state_name', 'county', 'latitude', 'longitude']].copy()
    # print(place_df.columns)
    # INSERT INTO evidence_dim
    # (incident_id, link)
    df['links'] = df['links'].astype(str)
    evidence_df = df[['id', 'links']].copy()
    evidence_df.to_sql('evidence_dim', con, if_exists='append',
                       index=False, method='multi')
    print(evidence_df.columns)


    # INSERT INTO force_tags_dim
    # (incident_id, force_tag)
<< << << < HEAD
tags = df[['id', 'tag_predicted']].copy()
tags.to_sql('tags', con,
            if_exists='append', index=False, method='multi')
print(tags.columns)
== == == =
force_tags_df = df[['id', 'tag_predicted']].copy()
force_tags_df.to_sql('force_tags_dim', con,
                     if_exists='append', index=False, method='multi')
print(force_tags_df.columns)
>>>>>> > 36f6c3cfc0ab29cdc9aa53ac2dd5fe021660d94c
