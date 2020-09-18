table = """
DROP TABLE IF EXISTS evidences;
CREATE TABLE IF NOT EXISTS evidences (
id serial PRIMARY KEY,
incident_id VARCHAR,
link VARCHAR,
FOREIGN KEY (incident_id) REFERENCES incidents (id)
);
"""
