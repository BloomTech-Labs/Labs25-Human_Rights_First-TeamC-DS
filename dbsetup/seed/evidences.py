def seed_table:
    # evidence: id, link
    with open('training_data.csv', 'r') as f:
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
            pg_curs, sql, data, template=None, page_size=10000)
