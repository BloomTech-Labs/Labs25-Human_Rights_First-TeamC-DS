import twitter
import urllib.parse
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv('../.env')
load_dotenv('../.env')

api = twitter.Api(consumer_key=os.getenv("CONSUMER_KEY"),
                  consumer_secret=os.getenv("CONSUMER_SECRET"),
                  access_token_key=os.getenv("ACCESS_TOKEN_KEY"),
                  access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
                  sleep_on_rate_limit=True)


if __name__ == "__main__":

    # The index includes between 6-9 days of Tweets.

    terms = [
        "police chokehold",
        "pepperspray",
        "rubber bullets",
        "tazed",
        "teargas",
        "police assualt",
        "mace",
        "police shooting",
        "police hitting",
        "police attack",
        "police hitting",
        "police bean bag",
        "police water hose",
        "police kneeling"
    ]
    term = "(" + ") OR (".join(terms) + ")"
    print(term)

    results = api.GetSearch(
        term=term,
        # geocode="-180,-90,180,90", need to find geocode for the USA???
        since="2019-08-01",
        lang="en",
        count=400)

    # for tweet in results:
    #     print(tweet)
    # print(len(results))


dbname = os.getenv("DB_DBNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)
# create cursor
pg_curs = pg_conn.cursor()
# pg_curs.execute('SELECT * FROM tweets;')
# pg_curs.fetchall()

create_table = """
CREATE TABLE IF NOT EXISTS tweets (
index SERIAL PRIMARY KEY,
name VARCHAR(30),
text VARCHAR,
location VARCHAR(30),
id INT,
created TIMESTAMP
);
"""
pg_curs.execute(create_table)

# show_tables = """
# SELECT *
# FROM pg_catalog.pg_tables
# WHERE schemaname !='pg_catalog'
# AND schemaname !='information_schema';
# """
for tweet in results:
    insert_tweet = """
  INSERT INTO tweets
  (name, text, location, id, created_at)
  VALUES """ + str([tweet.screen_name, tweet.text, tweet.location, tweet.id, tweet.created_at]) + ";"
    pg_curs.execute(insert_tweet)


pg_curs.fetchall()
