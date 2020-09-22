import psycopg2
from config import dbconfig
from tables import evidences as evidencesTable, incidents as incidentsTable, places as placesTable, tags as tagsTable
from seed import places, incidents, tags

cursor = psycopg2.connect(**dbconfig).cursor()

# cursor.execute(placesTable.query)
# cursor.execute(incidentsTable.query)
# cursor.execute(evidencesTable.query)
# cursor.execute(tagsTable.query)

# places.seed_table(cursor)
incidents.seed_table(cursor)
# tags.seed_table(cursor)

cursor.execute("COMMIT")
# pg_curs.fetchall()
cursor.close()
