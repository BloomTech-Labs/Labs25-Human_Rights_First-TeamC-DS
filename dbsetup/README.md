# Database

Data on police use of force for HRF is stored in relational tables managed with [PostgreSQL](https://www.postgresql.org). 

This directory contains scripts used for the setup and seeding of the database using [psycopg2](https://www.psycopg.org/docs/). The database was initially populated with the incidents in the provided `training_data` csv. Tables are defined in the tables subfolder, seed scrips are found in the seed subfolder, and setup is completed when running `db_postgresql.py`. 
