import twitter
import urllib.parse
import os
import psycopg2
import inspect
from dotenv import load_dotenv
load_dotenv('../.env')
load_dotenv('../.env')


dbname = os.getenv("DB_DBNAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
print(host, user, dbname)
pg_conn = psycopg2.connect(dbname=dbname, user=user,
                           password=password, host=host)
# create cursor
pg_curs = pg_conn.cursor()

# create the table structure
create_table = """
DROP TABLE IF EXISTS tweets;
CREATE TABLE IF NOT EXISTS tweets (
index SERIAL PRIMARY KEY,
name VARCHAR(30),
text VARCHAR,
location VARCHAR(30),
id BIGINT
);
"""
pg_curs.execute(create_table)


api = twitter.Api(consumer_key=os.getenv("CONSUMER_KEY"),
                  consumer_secret=os.getenv("CONSUMER_SECRET"),
                  access_token_key=os.getenv("ACCESS_TOKEN_KEY"),
                  access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
                  sleep_on_rate_limit=True)

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
    "police kneeling",
    "police brutality"
]
term = "(" + ") OR (".join(terms) + ")"

results = api.GetSearch(
    term=term,
    # geocode="-180,-90,180,90", geocode would go here but I have not found the right code to put here
    since="2019-08-01",
    lang="en",
    count=400)

for tweet in results:
    location = tweet.location
    if location is None:
        location
# insert into the table the twitter data from above
    insert_tweet = """
        INSERT INTO tweets
        (name, text, location, id)
        VALUES (%s, %s, %s, %s)
        """

    pg_curs.execute(insert_tweet,
                    (tweet.user.screen_name, tweet.text, tweet.location, tweet.id))

print(len(tweets))
# pg_curs.execute("COMMIT")

# pg_curs.fetchall()

# pg_curs.close()
