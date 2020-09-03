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

# incident dimension
create_incident_table = """
DROP TABLE IF EXISTS incident_dim CASCADE;
CREATE TABLE IF NOT EXISTS incident_dim (
index serial PRIMARY KEY,
incident_id VARCHAR UNIQUE,
edit_at VARCHAR,
text VARCHAR NOT NULL,
date VARCHAR,
city VARCHAR NOT NULL
);
"""


# place dimesion
# one to one with incident
create_place_table = """
DROP TABLE IF EXISTS place_dim;
CREATE TABLE IF NOT EXISTS place_dim (
incident_id VARCHAR,
city VARCHAR,
state_code CHAR(2),
state_name VARCHAR(30),
county VARCHAR(30),
latitude DECIMAL(9,6),
longitude DECIMAL(9,6),
FOREIGN KEY (incident_id) REFERENCES incident_dim (incident_id)
);
"""

# evidence dimesion
# many to one with incident
create_evidence_table = """
DROP TABLE IF EXISTS evidence_dim;
CREATE TABLE IF NOT EXISTS evidence_dim (
incident_id VARCHAR,
link VARCHAR,
PRIMARY KEY (incident_id),
FOREIGN KEY (incident_id) REFERENCES incident_dim (incident_id)
);
"""

# tags junction
# one to one with incident
create_tags_ref_table = """
DROP TABLE IF EXISTS tags_ref;
CREATE TABLE IF NOT EXISTS tags_ref (
index serial PRIMARY KEY,
tag VARCHAR(30)
);
"""

# force tags dimension
# many to one with tag junction id
# this table will also link to human tags once we expand to include those
create_force_tags_table = """
DROP TABLE IF EXISTS force_tags_dim;
CREATE TABLE IF NOT EXISTS force_tags_dim (
incident_id VARCHAR,
force_tag VARCHAR,
PRIMARY KEY (incident_id, force_tag),
FOREIGN KEY (incident_id) REFERENCES tags_dim (incident_id)
);
"""

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
pg_curs.execute(create_incident_table)
pg_curs.execute(create_place_table)
pg_curs.execute(create_evidence_table)
pg_curs.execute(create_tags_ref_table)
pg_curs.execute(create_force_tags_table)
# pg_curs.execute(create_human_tags_table)


# Stretch goals--add model to tag incoming data with human tags
# human tags dimension


# insert_human_tags = """
# INSERT INTO human_tags_dim
# (id, human_tag)
# VALUES (%s, %s)
# """


# function that inserts data into tables from training data csv
with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    # order: incident_id 6, text 4, edit_at 2, date 5, city 3
    data = []
    for row in reader:
        data.append([row[6], row[4], row[2], row[5], row[3]])
    sql = """
        INSERT INTO incident_dim
        (incident_id, text, edit_at, date, city)
        VALUES %s
        """
    psycopg2.extras.execute_values(
        pg_curs, sql, data, template=None, page_size=10000)

# place
with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    # order: id 6, city 3, state_code 7 , state_name 1 , county 28 , latitude9 , longitude10
    data = []
    for row in reader:
        data.append([row[6], row[3], row[7], row[1],
                     row[8], row[9], row[10]])
    sql = """
        INSERT INTO place_dim
        (incident_id, city, state_code, state_name, county, latitude, longitude)
        VALUES %s
        """
    psycopg2.extras.execute_values(
        pg_curs, sql, data, template=None, page_size=10000)

# evidence: id, link
with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    data = []
    for row in reader:
        data.append([row[6], row[13]])

    sql = """
        INSERT INTO evidence_dim
        (incident_id, link)
        VALUES %s
        """
    psycopg2.extras.execute_values(
        pg_curs, sql, data, template=None, page_size=10000)


# Force tags junction (same as force tags right now until we add human tags)
with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    data = []
    for row in reader:
        data.append([row[6], row[12]])
    sql = """
        INSERT INTO force_tags_dim
        (incident_id, force_tag)
        VALUES %s
        """
    psycopg2.extras.execute_values(
        pg_curs, sql, data, template=None, page_size=10000)

# Force tags listed with index 1-9

data = [['Presence'], ['Verbal'], ['EHC Soft Technique'], ['EHC Hard Technique'],
        ['Blunt Impact'], ['Chemical'], ['Projectile'], ['CED'], ['Other/Unknown']]

sql = """
      INSERT INTO tags_ref
      (tag)
      VALUES %s
       """
psycopg2.extras.execute_values(
    pg_curs, sql, data, template=None, page_size=10000)


pg_curs.execute("COMMIT")

# pg_curs.fetchall()

pg_curs.close()
