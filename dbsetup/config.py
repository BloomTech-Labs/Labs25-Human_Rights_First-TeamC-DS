import os
from dotenv import load_dotenv
load_dotenv('../.env')

dbname = os.getenv("DB_DBNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")

dbconfig = dict(dbname, user, password, host)
