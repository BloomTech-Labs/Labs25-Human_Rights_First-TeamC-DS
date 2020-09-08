# imports
import pandas as pd
import re
import geopy
from geopy.geocoders import Nominatim # Nominatim geocoding (built on OpenStreetMap data)
from geopy.extra.rate_limiter import RateLimiter

# police use of force data
pb_csv = pd.read_csv('https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations.csv')
pb_df = pd.DataFrame(pb_csv)

### clean ### 
def clean_pb2020(df):
    '''
    function that takes PB2020 api data
    processes it according to our project needs
    outputs a cleaned df
    '''
    # rename columns (location columns to loc standard and description column to 'text')
    df.rename(columns={'state':'STATE_NAME', 'city':'CITY', 'name':'text'}, inplace=True)
    # drop redundant date column
    df = df.drop('date_text', axis=1)
    # change substandard city and state names
    df['CITY']= df['CITY'].str.replace('New York City', 'New York', case = False)
    df['CITY']= df['CITY'].str.replace('DC', 'Washington', case = True)
    df['STATE_NAME']= df['STATE_NAME'].str.replace('Washington DC', 'District of Columbia', case = False)
    # drop NaNs
    df.dropna(subset = ['CITY', 'date'], inplace=True)
    # put date column in datetime
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
    # remove leading and trailing whitespace from columns
    df['CITY'] = df['CITY'].str.strip()
    df['STATE_NAME'] = df['STATE_NAME'].str.strip()
    # combine evidence columns which aren't empty into a new column
    links = ['Link 1', 'Link 2', 'Link 3', 'Link 4', 'Link 5', 'Link 6', 'Link 7', 'Link 8', 'Link 9', 'Link 10', 
    'Link 11', 'Link 12', 'Link 13', 'Link 14', 'Link 15', 'Link 16', 'Link 17', 'Link 18', 'Link 19', 'Link 20']
    df['links'] = df[links].agg(lambda x: x.dropna().tolist(), axis=1)
    # drop old evidence columns
    df = df.drop(links, axis=1)
    # put description column into str and convert text to lowercase
    df['text'] = df['text'].astype(str).str.lower()
    # regex for nlp:
    # remove backslash and apostrophe
    df['text'] = df['text'].str.replace(r'\'', r'')
    # remove anything that isn't in a-z
    df['text'] = df['text'].str.replace(r'[^a-zA-Z]', r' ')

    return df

# apply clean fxn
pb_df = clean_pb2020(pb_df)

### add geolocation data ###
def geoloc(df):
    '''
    function that adds geolocation data
    given city of incident
    outputs df with lat and long columns
    '''
    # Nominatim for geocoding
    locator = Nominatim(user_agent="myGeocoder")
    # delay geocoding by 1 second between each incident to avoid rate limit
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    # create column of city, state to apply geocode to
    df['city_state'] = df['CITY'].astype(str) + ',' + df['STATE_NAME']
    # create column by applying geocode
    df['location'] = df['city_state'].apply(geocode)
    # create lat, long, altitude as a single tuple column via pulling that data from location column
    df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
    # split latitude, longitude, and altitude columns into three separate columns
    df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)
    # drop unnecessary columns
    df = df.drop(['altitude', 'location', 'point', 'city_state'], axis=1)

    return df

# apply geolocation fxn
pb_df = geoloc(pb_df)