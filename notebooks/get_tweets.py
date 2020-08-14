#code will go in here
import urllib.parse
import twitter
from dotenv import load_dotenv
load_dotenv()



api = twitter.Api(consumer_key=os.getenv("CONSUMER_KEY"),
                  consumer_secret=os.getenv("CONSUMER_SECRET"),
                  access_token_key=os.getenv("ACCESS_TOKEN_KEY"),
                  access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
                  sleep_on_rate_limit=True)


if __name__ == "__main__":

#The index includes between 6-9 days of Tweets.



    results = api.GetSearch(
        term="(police chokehold) OR (pepperspray) OR (rubber bullets) OR (tazed) OR (teargas) OR (police assualt) OR (mace) OR (police shooting) OR (police hitting) OR (police attack)",
        #geocode="-180,-90,180,90", need to find geocode for the USA???
        since="2019-08-01",
        lang="en",
        total_count=100)
    for tweet in results:
        print(tweet)
    print(len(results))
