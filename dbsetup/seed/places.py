import csv
import psycopg2
from ..db_postgresql import cursor


def seed_table():
    with open('../training_data.csv', 'r') as f:
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
                cache[place]['lat'],
                cache[place]['lon'],
                cache[place]['counter']])

        sql = """
            INSERT INTO places
            (city, state_code, state_name, latitude, longitude, counter)
            VALUES %s
            """
        psycopg2.extras.execute_values(cursor, sql, params, page_size=10000)
