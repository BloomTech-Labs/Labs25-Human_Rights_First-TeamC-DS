query = """
DROP TABLE IF EXISTS places CASCADE;
CREATE TABLE IF NOT EXISTS places (
id SERIAL PRIMARY KEY,
city VARCHAR,
state_code CHAR(2),
state_name VARCHAR(30),
latitude DECIMAL(9,6),
longitude DECIMAL(9,6),
counter INT
);
"""
