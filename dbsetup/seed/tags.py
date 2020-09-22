# tags table
import pandas as pd


def seed_table(pg_curs):
    df = pd.read_csv('dbsetup/training_data.csv')
    # Separates the tags by category into different rows
    df = df.explode('force_tags')
    df = df[['id', 'force_tags']]
    df.to_sql('tags', pg_curs)


with open('dbsetup/training_data.csv', 'r') as f:
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
