import csv
import psycopg2
from ..db_postgresql import cursor


def seed_table():
    with open('../training_data.csv', 'r') as f:
        reader = csv.reader(f)
        next(f)
        # incidents
        # order: id 6, text 4, edit_at 2, date 5, city 3
        data = []
        # gets the correct place ID in our database that matches the incident

        # 1. Query entire places table
        # slap that sucker into nested dictionary
        # lookup by statecode, and then look up by city
        # if the incident state/city is not there,
        # make a query to create a new place
        # else:
        # check if the amount of incidents is greater

        # there is already a new

        # 2. Query places table for each incident to check
        # does SQL have a way to combine multiple checks into one?

        # incident is ma-boston-1
        # incident split by '-'

        for row in reader:
            data.append([row[6], row[4], row[5]])
        sql = """
            INSERT INTO incidents
            (id, text, date)
            VALUES %s
            """
        psycopg2.extras.execute_values(
            pg_curs, sql, data, template=None, page_size=10000)
