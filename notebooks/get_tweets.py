# This page is now redundant and can be deleted soon.
# Its useful to play with the twitter API without having to create a new table and update ElephantSQL
# see Data folder for Elephant SQL with twitter data

import os
import urllib.parse
import twitter
from dotenv import load_dotenv
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

    results = api.GetSearch(
        term=term,
        # geocode="-180,-90,180,90", need to find geocode for the USA???
        since="2019-08-01",
        lang="en",
        count=10)

    for tweet in results:
        print([tweet])
        print(tweet.name)
    # print(len(results))
