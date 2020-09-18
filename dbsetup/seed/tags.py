# tags table
def seed_table():
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

# sql = """
#       INSERT INTO tags
#       (force_tag)
#       VALUES %s
#        """
# psycopg2.extras.execute_values(
#     pg_curs, sql, data, template=None, page_size=10000)



data = [['Presence'], ['Verbal'], ['EHC Soft Technique'], ['EHC Hard Technique'],
        ['Blunt Impact'], ['Chemical'], ['Projectile'], ['CED'], ['Other/Unknown']]
