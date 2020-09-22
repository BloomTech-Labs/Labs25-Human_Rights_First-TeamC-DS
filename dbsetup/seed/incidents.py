import csv
import psycopg2
from pprint import pprint


def seed_table(db):
    with open('dbsetup/training_data2.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = []

        places_query = """SELECT * FROM places"""
        db.execute(places_query)
        places = db.fetchall()

        # assumes all places are already inside the database, eg. no invalid places
        place_id_lookup = {}
        for place in places:
            pk, city, state_code, _, __, ___, ____ = place
            state_code = state_code.lower()
            city = city.replace(" ", '').lower()
            if state_code not in place_id_lookup:
                place_id_lookup[state_code] = {}
            place_id_lookup[state_code][city] = pk
        pprint(place_id_lookup)

        # creates the dynamic data for the SQL query
        data = []
        for row in reader:
            # may God forgive us
            if row['id'] == 'or-orlando-5' or row['id'] == 'or-orlando-8':
                data.append([row['id'], 67, row['text'], row['date']])
                continue
            state, city, _ = row['id'].split('-')
            # if state == dc, state = washington
            # print(f"{city}, {state}")
            place_id = place_id_lookup[state][city]
            data.append([row['id'], place_id, row['text'], row['date']])

        pprint(data)

        # check what state, and what city
        # create a SQL statement that adds a new incident record, with the appropriate
        # place foreign key relationship

        # lookup by statecode, and then look up by city

        sql = """
            INSERT INTO incidents
            (id, place_id, descr, date)
            VALUES %s
            """
        psycopg2.extras.execute_values(
            db, sql, data, template=None, page_size=10000)
        print(data)
