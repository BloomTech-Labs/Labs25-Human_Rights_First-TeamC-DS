import urllib.parse
import psycopg2
from .config import dbconfig
from .tables import evidences, incidents, places, tags
from .seed import places

cursor = psycopg2.connect(**dbconfig).cursor()

cursor.execute(evidences.table)
cursor.execute(incidents.table)
cursor.execute(places.table)
cursor.execute(tags.table)

places.seed_table()
incidents.seed_table()


# tags table
with open('training_data.csv', 'r') as f:
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


# we need to get the force tags for new incoming data from main.py and read it here.
# psuedocode for the tags
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

# # pg_curs.fetchall()

pg_curs.close()
