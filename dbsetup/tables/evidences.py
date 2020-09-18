create_evidence_table = """
DROP TABLE IF EXISTS evidence;
CREATE TABLE IF NOT EXISTS evidence (
id serial PRIMARY KEY,
incident_id VARCHAR,
link VARCHAR,
FOREIGN KEY (incident_id) REFERENCES incidents (id)
);
"""
