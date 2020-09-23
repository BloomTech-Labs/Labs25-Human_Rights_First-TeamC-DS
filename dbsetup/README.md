# Database

Data on police use of force for HRF is stored in relational tables managed with PostgreSQL. 

This directory contains scripts used for the setup and seeding of the database. The database was initially populated with the incidents in the provided `training_data` csv. Tables are defined in the tables subfolder, seed scrips are found in the seed subfolder, and setup is completed when running `db_postgresql.py`. 


## Prerequisites

First, install **PostgreSQL** from [the following page.](https://www.postgresql.org/download/)

Second, to install python dependencies, run:

``` pip install psycopg2 ```  

