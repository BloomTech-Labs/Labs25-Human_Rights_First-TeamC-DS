# imports & connection
import urllib.parse
import os
import psycopg2
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
pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)
# create cursor
pg_curs = pg_conn.cursor()

### create tables ###

# incident dimension
create_incident_table = """
DROP TABLE IF EXISTS incident_dim;
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
city serial PRIMARY KEY,
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
create_tags_table = """
DROP TABLE IF EXISTS tags_dim;
CREATE TABLE IF NOT EXISTS tags_dim (
incident_id VARCHAR,
force_tag VARCHAR,
PRIMARY KEY (incident_id),
FOREIGN KEY (incident_id) REFERENCES incident_dim (incident_id)
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
FOREIGN KEY (incident_id) REFERENCES tags_dim (incident_id),
FOREIGN KEY (force_tag) REFERENCES tags_dim (incident_id)
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
pg_curs.execute(create_tags_table)
pg_curs.execute(create_force_tags_table)
# pg_curs.execute(create_human_tags_table)


### insert data into tables ###

# incident dimension
insert_incident = """
INSERT INTO incident_dim
(incident_id, text, edit_at, date, city)
VALUES (%s, %s, %s, %s, %s)
"""

# place dimension
insert_place = """
INSERT INTO place_dim
(id, city, state_code, state_name, county, latitude, longitude)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
# will also need CRONJOP info added later

# evidence dimension
# HOW TO SEPERATE LINKS FROM DIFFERENT CSV COLUMNS INTO THIS TABLE
insert_evidence = """
INSERT INTO evidence_dim
(id, link)
VALUES (%s, %s)
"""

# tags junction
insert_tags = """
INSERT INTO tags_dim
(id, force_tags)
VALUES (%s, %s)
"""

# will need model run before for new data from CRONJOB
# force tags dimension
# HOW TO SEPERATE COMMA SEPERATED TAGS FOR INSERTION INTO THIS TABLE
insert_force_tags = """
INSERT INTO force_tags_dim
(id, force_tag)
VALUES (%s, %s)
"""

# Stretch goals--add model to tag incoming data with human tags
# human tags dimension
# HOW TO SEPERATE COMMA SEPERATED TAGS FOR INSERTION INTO THIS TABLE
# insert_human_tags = """
# INSERT INTO human_tags_dim
# (id, human_tag)
# VALUES (%s, %s)
# """


# .copy_from method requires csv to be the same columns as the SQL table

# function that inserts data into tables from training data csv

with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    for row in reader:
        print(row)
        pg_curs.execute(insert_incident, [
                        row[7], row[5], row[3], row[6], row[4]])

# place : id, city[2], state_code[27], state_name[0], county[28], latitude[29], longitude[30]
with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    for row in reader:
        pg_curs.execute(
            insert_place, [row[5], row[27], row[0], row[28], row[29], row[30]])

# evidence: id, link
with open('/Users/michelle/Labs25-Human_Rights_First-TeamC-DS/Data/training_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(f)  # skipping the header row
    for row in reader:
        pg_curs.execute(insert_evidence, [row[5], row[6]])
        pg_curs.execute(insert_tags, [row[5], row[31]])
        pg_curs.execute(insert_force_tags, [row[5], row[31]])


pg_curs.execute("COMMIT")

pg_curs.fetchall()

pg_curs.close()
