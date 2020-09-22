def seed_table(conn):
    # evidence: id, link
    with open('dbsetup/training_data2.csv', 'r') as f:
        reader = csv.reader(f)
        next(f)  # skipping the header row
        # order: id 6, link 13
        data = []
        for row in reader:
            data.append([row[6], row[13]])

        sql = """
                INSERT INTO evidence
                (incident_id, link)
                VALUES %s
                """
        psycopg2.extras.execute_values(
            conn, sql, data, template=None, page_size=10000)
