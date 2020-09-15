import urllib.parse
from pprint import pprint
import os
import psycopg2
import psycopg2.extras
import inspect
import csv
from dotenv import load_dotenv
load_dotenv('../.env')

dbname = os.getenv("DB_DBNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")

pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)
pg_curs = pg_conn.cursor()

create_place_table = """
DROP TABLE IF EXISTS places CASCADE;
CREATE TABLE IF NOT EXISTS places (
id SERIAL PRIMARY KEY,
city VARCHAR,
state_code CHAR(2),
state_name VARCHAR(30),
county VARCHAR(30),
latitude DECIMAL(9,6),
longitude DECIMAL(9,6),
counter INT
);
"""

# incident dimension
create_incident_table = """
DROP TABLE IF EXISTS incidents CASCADE;
CREATE TABLE IF NOT EXISTS incidents (
id VARCHAR PRIMARY KEY,
place_id INT,
edit_at VARCHAR,
text VARCHAR NOT NULL,
date VARCHAR,
FOREIGN KEY (place_id) REFERENCES places (id)
);
"""

create_evidence_table = """
DROP TABLE IF EXISTS evidence;
CREATE TABLE IF NOT EXISTS evidence (
id serial PRIMARY KEY,
incident_id VARCHAR,
link VARCHAR,
FOREIGN KEY (incident_id) REFERENCES incidents (id)
);
"""

create_tags_table = """
DROP TABLE IF EXISTS tags;
CREATE TABLE IF NOT EXISTS tags (
id serial PRIMARY KEY,
incident_id VARCHAR,
tag VARCHAR,
FOREIGN KEY (incident_id) REFERENCES incidents (id)
);
"""

# human tags dimension
# many to one with tag junction id
create_human_tags_table = """
DROP TABLE IF EXISTS human_tags_dim;
CREATE TABLE IF NOT EXISTS human_tags_dim (
PRIMARY KEY (human_dim_id),
FOREIGN KEY (tags_id) REFERENCES tags_dim(tags_id),
human_tag VARCHAR(30)
);
"""


# create the tables
pg_curs.execute(create_place_table)
print('dropping table if exists')
pg_curs.execute(create_incident_table)
pg_curs.execute(create_evidence_table)
pg_curs.execute(create_tags_table)
# pg_curs.execute(create_force_tags_table) #still deciding what to do with this one
# pg_curs.execute(create_human_tags_table) #not yet implemented this data

# Stretch goals--add model to tag incoming data with human tags

# Place seed
with open('training_data.csv', 'r') as f:
    reader = csv.DictReader(f)
    cache = {}
    for row in reader:
        splitRow = row['id'].split('-')
        location = f'{splitRow[0]}{splitRow[1]}'
        if location in cache:
            cache[location]['counter'] += 1
        else:
            cache[location] = {
                'cityName': row['CITY'],
                'stateName': row['STATE_NAME'],
                'stateCode': row['STATE_CODE'],
                'county': row['COUNTY'],
                'lat': row['LATITUDE'],
                'lon': row['LONGITUDE'],
                'counter': 1
            }

    params = []
    for place in cache:
        params.append([
            cache[place]['cityName'],
            cache[place]['stateCode'],
            cache[place]['stateName'],
            cache[place]['county'],
            cache[place]['lat'],
            cache[place]['lon'],
            cache[place]['counter']])

    sql = """
        INSERT INTO places
        (city, state_code, state_name, county, latitude, longitude, counter)
        VALUES %s
        """
    psycopg2.extras.execute_values(
        pg_curs, sql, params, page_size=10000)

# function that inserts data into tables from training data csv
with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    # incidents
    # order: id 6, text 4, edit_at 2, date 5, city 3
    data = []
    for row in reader:
        data.append([row[6], row[4], row[2], row[5]])
    sql = """
        INSERT INTO incidents
        (id, text, edit_at, date)
        VALUES %s
        """
    psycopg2.extras.execute_values(
        pg_curs, sql, data, template=None, page_size=10000)


# evidence: id, link
with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    # order: id 6, link 13
    data = []
    for row in reader:
        data.append([row[6], row[13]])

    sql = """
        INSERT INTO evidence
        (incident_id, link)
        VALUES %s
        """
    psycopg2.extras.execute_values(
        pg_curs, sql, data, template=None, page_size=10000)


# tags table
with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    # order: id 6, tag 12
    data = []
    for row in reader:
        data.append([row[6], row[12]])

    sql = """
        INSERT INTO tags
        (incident_id, tag)
        VALUES %s
        """
    psycopg2.extras.execute_values(
        pg_curs, sql, data, template=None, page_size=10000)


# we need to get the force tags for new incoming data from main.py and read it here.
# psuedocode for the tags
    # data = []
    # for row in tags_function():
    #     if tag == 'Projectile'
    #     data.append(row.id, row.tag)
    # sql = """
    #     INSERT INTO force_tags_dim
    #     (incident_id, force_tag, tag_id)
    #     VALUES %s
    #     """
    # psycopg2.extras.execute_values(
    #     pg_curs, sql, data, template=None, page_size=10000)

# Force tags listed with index 1-9

# data = [['Presence'], ['Verbal'], ['EHC Soft Technique'], ['EHC Hard Technique'],
#         ['Blunt Impact'], ['Chemical'], ['Projectile'], ['CED'], ['Other/Unknown']]

# sql = """
#       INSERT INTO tags
#       (force_tag)
#       VALUES %s
#        """
# psycopg2.extras.execute_values(
#     pg_curs, sql, data, template=None, page_size=10000)


pg_curs.execute("COMMIT")

# # pg_curs.fetchall()

pg_curs.close()
