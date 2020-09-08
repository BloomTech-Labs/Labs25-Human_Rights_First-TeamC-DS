# imports
import pandas as pd
import re

# police brutality data
# pb_csv = pd.read_csv('https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations.csv')
# pb_df = pd.DataFrame(pb_csv)

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
    df['CITY']= df['CITY'].str.replace('Hollywood', 'Los Angeles', case = True)
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

### location data ###
loc_csv = pd.read_csv('https://raw.githubusercontent.com/kelvins/US-Cities-Database/main/csv/us_cities.csv')
loc_df = pd.DataFrame(loc_csv)

def clean_loc(df):
    '''
    function that cleans and processes location data
    '''
    # drop redundant id column in loc_df
    df = df.drop('ID', axis=1)
    # drop rows with the same city and state but different counties
    df = df.drop_duplicates(subset=['STATE_CODE','CITY'], keep='first')
    # add missing cities
    Ferguson = {'STATE_CODE':'MO' ,'STATE_NAME':'Missouri', 'CITY':'Ferguson', 'COUNTY':'St. Louis', 'LATITUDE':38.744167, 'LONGITUDE':-90.305278}
    DC = {'STATE_CODE':'DC' ,'STATE_NAME':'District of Columbia', 'CITY':'Washington', 'COUNTY':'St. Louis', 'LATITUDE':38.912217, 'LONGITUDE':-77.017691}
    df = df.append(Ferguson, ignore_index=True)
    df = df.append(DC, ignore_index=True)

    return df

# apply location clean fxn
loc_df = clean_loc(loc_df)

### merge ###
def merge_loc(df):
    '''
    adds location data to the PB2020 incidents
    creates a new df of the combined data
    '''
    df = pb_df.merge(loc_df, how='inner')
    # drop any incidents that got duplicated
    df = df.drop_duplicates(subset=['id'], keep='last')

    return df
