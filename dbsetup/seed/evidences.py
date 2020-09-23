import csv
import psycopg2
from pprint import pprint

def seed_table(conn):
    # evidence: id, link
    with open('dbsetup/training_data.csv', 'r') as f:
        reader = csv.reader(f)
        next(f)  # skipping the header row
        # order: id 6, link 13
        data = []
        for row in reader:
            # Converts strings like this:
            # ['a', 'b', 'c']
            # ..into a Python list of strings
            links = row[13][2:-2].split("', '")
            for link in links:
                data.append([row[6], link])
        sql = """
            INSERT INTO evidences
            (incident_id, link)
            VALUES %s
            """
        psycopg2.extras.execute_values(
            conn, sql, data, template=None, page_size=10000)