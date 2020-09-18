# imports
import pandas as pd
import re
import geopy
# Nominatim geocoding (built on OpenStreetMap data)
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
# db
from ..database import SessionLocal, engine
from sqlalchemy.orm import Session
from util.constants import EVIDENCES_TABLE

router = APIRouter()
con = engine.connect()


def get_new(new_df):
    '''
    function that updates evidence for exsisting incidents
    and gets new incidents
    outputs df of new incidents and old incidents w/ new links column values
    '''
    # df of existing db data
    db_df = pd.read_sql(f'SELECT * FROM ${EVIDENCES_TABLE}', con)
    # section of new data that MATCHES our database by id
    match = new_df[new_df['id'].isin(db_df['id'])]
    # set new df = NEW incident IDs aka incidents that were NOT in our db
    new_df = new_df[~new_df['id'].isin(db_df['id'])]
    # TODO: append old incidents that had new evidence links to new_df

    return new_df


def clean_pb2020(df):
    '''
    function that takes PB2020 api data
    processes it according to our project needs
    outputs a cleaned df
    '''
    # rename columns (location columns to loc standard and description column to 'text')
    df.rename(columns={'state': 'STATE_NAME',
                       'city': 'CITY', 'name': 'text'}, inplace=True)
    # drop redundant date column
    df = df.drop('date_text', axis=1)
    # change substandard city and state names
    df['CITY'] = df['CITY'].str.replace(
        'New York City', 'New York', case=False)
    df['CITY'] = df['CITY'].str.replace('DC', 'Washington', case=True)
    df['STATE_NAME'] = df['STATE_NAME'].str.replace(
        'Washington DC', 'District of Columbia', case=False)
    # drop NaNs
    df.dropna(subset=['CITY', 'date'], inplace=True)
    # put date column in datetime
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
    # remove leading and trailing whitespace from columns
    df['CITY'] = df['CITY'].str.strip()
    df['STATE_NAME'] = df['STATE_NAME'].str.strip()
    # create column for state abbreviations
    df['state_code'] = df['id'].str.split('-').str[0]
    # ensure state code column is str and capitalized
    df['state_code'] = df['state_code'].astype(str).str.upper()
    # put description column into str and convert text to lowercase
    df['text'] = df['text'].astype(str).str.lower()
    # regex for nlp:
    # remove backslash and apostrophe
    df['text'] = df['text'].str.replace(r'\'', r'')
    # remove anything that isn't in a-z
    df['text'] = df['text'].str.replace(r'[^a-zA-Z]', r' ')

    return df


def geoloc(df):
    '''
    Mutates a dataframe and adds geolocation data (lat/lon columns) based on city of incident
    '''
    locator = Nominatim(user_agent="myGeocoder")
    # delay geocoding by 1 second between each incident to avoid rate limit
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    df['city_state'] = df['CITY'].astype(str) + ',' + df['STATE_NAME']
    df['location'] = df['city_state'].apply(geocode)
    # create lat, long, altitude as a single tuple column via pulling that data from location column
    df['point'] = df['location'].apply(
        lambda loc: tuple(loc.point) if loc else None)
    # split latitude, longitude, and altitude columns into three separate columns
    df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(
        df['point'].tolist(), index=df.index)
    # drop unnecessary columns
    df = df.drop(['altitude', 'location', 'point', 'city_state'], axis=1)

    return df
