import urllib.parse
from twitter_api import api


if __name__ == "__main__":
#     results = api.GetSearch(raw_query="q=twitter%20&result_type=recent&since=2014-07-19&count=100")
#The index includes between 6-9 days of Tweets.

#Geolocalization: the search operator “near” isn’t available in the API, but there is a more precise way to restrict your query by a given location using the geocode parameter specified with the template “latitude,longitude,radius”, for example, “37.781157,-122.398720,1mi”. When conducting geo searches, the search API will first attempt to find Tweets which have lat/long within the queried geocode, and in case of not having success, it will attempt to find Tweets created by users whose profile location can be reverse geocoded into a lat/long within the queried geocode, meaning that is possible to receive Tweets which do not include lat/long information

    q = "police chokehold"
    results = api.GetSearch(raw_query="q=" + urllib.parse.quote(q) + "%20lang%3Aen%20since%3A2019-08-01")
    results = api.GetSearch(raw_query="https://api.twitter.com/1.1/search/tweets.json?q=police%2Bpepper-spray&src=typed_query")
    
    
    for tweet in results:
        print(tweet)