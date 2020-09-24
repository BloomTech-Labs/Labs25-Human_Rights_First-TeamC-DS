# Database

Data on police use of force for HRF is stored in relational tables managed with [PostgreSQL](https://www.postgresql.org). 

This directory contains scripts used for the setup and seeding of the database using [psycopg2](https://www.psycopg.org/docs/). The database was initially populated with the incidents in the provided `training_data` csv. Tables are defined in the tables subfolder, seed scrips are found in the seed subfolder, and setup is completed when running `db_postgresql.py`. 

## Data Source 

Our training data is from [Police Brutality 2020](https://github.com/2020PB/police-brutality) as of August 2020, which primarily sources data from Reddit posts. We began this project with the intention of using tweets from the Twitter API, but decided to use PB2020 to start with due to Twitter's lack of location metadata on Tweets as of 2019. One of our goals for future releases is to include more direct social media scraping for data collection, which will likely need an additional model built to predict location. The notebooks containing the code which cleaned and processed the PB2020 data in order to create our training dataset can be found in the [notebooks](./notebooks/) section of this repository.

## Database Schema

<img src="https://raw.githubusercontent.com/Lambda-School-Labs/Labs25-Human_Rights_First-TeamC-DS/main/dbssetup/DB_Schema.png" width = "500">