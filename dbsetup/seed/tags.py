# tags table
import csv
from pprint import pprint
import psycopg2

def seed_table(pg_curs):
    with open('dbsetup/training_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        # order: id 6, tag 12
        data = []
        for row in reader:
            for tag in row['force_tags'].split(','):
                data.append([row['id'],tag.strip()])

        sql = """
            INSERT INTO tags
            (incident_id, tag)
            VALUES %s
            """
        psycopg2.extras.execute_values(
            pg_curs, sql, data, template=None, page_size=10000)
