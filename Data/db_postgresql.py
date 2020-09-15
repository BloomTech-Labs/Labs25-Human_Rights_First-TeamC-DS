# imports & connection
import urllib.parse
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
print(host, user, dbname)

# initiate connection
"""
psycopg2 is a PostgreSQL database adapter for the Python programming
language.  psycopg2 was written with the aim of being very small and fast,
and stable as a rock.
psycopg2 is different from the other database adapter because it was
designed for heavily multi-threaded applications that create and destroy
lots of cursors and make a conspicuous number of concurrent INSERTs or
UPDATEs. psycopg2 also provide full asynchronous operations and support
for coroutine libraries.
"""
pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)
# create cursor
pg_curs = pg_conn.cursor()

### create tables ###

# place dimension

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

# evidence dimesion
# one to many
create_evidence_table = """
DROP TABLE IF EXISTS evidence;
CREATE TABLE IF NOT EXISTS evidence (
id serial PRIMARY KEY,
incident_id VARCHAR,
link VARCHAR,
FOREIGN KEY (incident_id) REFERENCES incidents (id)
);
"""

# tags junction
create_tags_table = """
DROP TABLE IF EXISTS tags;
CREATE TABLE IF NOT EXISTS tags (
id serial PRIMARY KEY,
incident_id VARCHAR,
tag VARCHAR,
FOREIGN KEY (incident_id) REFERENCES incidents (id)
);
"""
#below is code that is still a work in progress

# human tags dimension
# many to one with tag junction id
# create_human_tags_table = """
# DROP TABLE IF EXISTS human_tags_dim;
# CREATE TABLE IF NOT EXISTS human_tags_dim (
# PRIMARY KEY (human_dim_id),
# FOREIGN KEY (tags_id) REFERENCES tags_dim(tags_id),
# human_tag VARCHAR(30)
# );
# """


# create the tables
pg_curs.execute(create_place_table)
pg_curs.execute(create_incident_table)
pg_curs.execute(create_evidence_table)
pg_curs.execute(create_tags_table)
#pg_curs.execute(create_force_tags_table) #still deciding what to do with this one
# pg_curs.execute(create_human_tags_table) #not yet implemented this data


# Stretch goals--add model to tag incoming data with human tags
# human tags dimension


# # place
with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    # order: id 6, city 3, state_code 7 , state_name 1 , county 28 , latitude9 , longitude10
    data = []
    for row in reader:
        data.append([row[3], row[7], row[1],
                     row[8], row[9], row[10]])
    sql = """
        INSERT INTO places
        (city, state_code, state_name, county, latitude, longitude)
        VALUES %s
        """
    psycopg2.extras.execute_values(
        pg_curs, sql, data, template=None, page_size=10000)

# function that inserts data into tables from training data csv
with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    #incidents
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
    #order: id 6, link 13
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
    #order: id 6, tag 12
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


#we need to get the force tags for new incoming data from main.py and read it here.
#psuedocode for the tags
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

# pg_curs.fetchall()

pg_curs.close()
