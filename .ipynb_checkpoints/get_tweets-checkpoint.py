import urllib.parse
from twitter_api import api


if __name__ == "__main__":
#     results = api.GetSearch(raw_query="q=twitter%20&result_type=recent&since=2014-07-19&count=100")
    q = "police chokehold"
    results = api.GetSearch(raw_query="q=" + urllib.parse.quote(q) + "%20lang%3Aen%20since%3A2019-08-01")
    for tweet in results:
        print(tweet)