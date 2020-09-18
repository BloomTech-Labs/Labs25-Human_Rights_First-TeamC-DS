import csv
import psycopg2
from pprint import pprint


def seed_table(db):
    with open('dbsetup/training_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        data = []

        # gets the correct place ID in our database that matches the incident
        places_query = """SELECT * FROM places"""
        db.execute(places_query)
        places = db.fetchall()

        places_keys = ['id', 'city', 'state_code',
                       'state_name', 'latitde', 'longitude', 'counter']
        place_id_lookup = {place[2]: {
            place[1]: place[0]} for place in places}

        data = {}
        pprint(place_id_lookup)
        for row in reader:
            # get the places id from placesLookUp
            place_id = place_id_lookup[row['STATE_CODE']][row['CITY']]
            if place_id in data:
                data[place_id] += 1
            else:
                data[place_id] = 1
        pprint(data)

        # check what state, and what city
        # create a SQL statement that adds a new incident record, with the appropriate
        # place foreign key relationship

        # lookup by statecode, and then look up by city
        # For seeding, no need to check for new location

        # sql = """
        #     INSERT INTO incidents
        #     (id, text, date)
        #     VALUES %s
        #     """
        # psycopg2.extras.execute_values(conn, sql, data, template = None, page_size = 10000)
        # print(data)
