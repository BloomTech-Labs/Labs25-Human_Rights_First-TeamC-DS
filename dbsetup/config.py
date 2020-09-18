import os
from dotenv import load_dotenv
load_dotenv('./project/app/.env')

dbname = os.getenv("DB_DBNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")

dbconfig = {'dbname': dbname, 'user': user, 'password': password, 'host': host}
