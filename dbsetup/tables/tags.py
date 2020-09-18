create_tags_table = """
DROP TABLE IF EXISTS tags;
CREATE TABLE IF NOT EXISTS tags (
id serial PRIMARY KEY,
incident_id VARCHAR,
tag VARCHAR,
FOREIGN KEY (incident_id) REFERENCES incidents (id)
);
"""
