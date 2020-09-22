import pandas as pd

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
    # df = df.drop('date_text', axis=1)
    # change substandard city and state names
    df['CITY'] = df['CITY'].str.replace('DC', 'Washington', case=True)
    df['STATE_NAME'] = df['STATE_NAME'].str.replace(
        'Washington DC', 'District of Columbia', case=False)
    df['CITY'] = df['CITY'].str.replace(
        'Hungtington Beach', 'Huntington Beach', case=True)
    # fix id to match city name
    df['id'] = df['id'].replace({'-dc': '-washington'}, regex=True)
    df['id'] = df['id'].replace(
        {'-hungtingtonbeach': '-huntingtonbeach'}, regex=True)
    df['id'] = df['id'].replace({'-costa-mesa': '-costamesa'}, regex=True)
    df['id'] = df['id'].replace({'-newyorkcity': '-newyork'}, regex=True)
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
    df['CITY'] = df['CITY'].str.replace(r'[^a-zA-Z]', r' ')
    df['text'] = df['text'].str.replace(r'[^a-zA-Z]', r' ')

    return df


df = pd.read_csv('dbsetup/training_data.csv')

df = clean_pb2020(df)

df.to_csv('dbsetup/training_data2.csv')