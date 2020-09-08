import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode

def lambda_handler(event=None, context=None):
    '''
    Lambda function that gets data from the 2020PB api
    and sends it to a designated endpoint from ds api
    '''
    # requests pb2020 api
    content = urlopen('https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations.json').read().decode('utf-8')
    alldata = json.loads(content)

    data = alldata['data']

    cron_update_url = 'http://localhost:8000/cron_update/'

    jsondata = json.dumps(data)
    jsonbytes = jsondata.encode('utf-8')
    cron_update_request = Request(cron_update_url, jsonbytes)
    cron_update_request.add_header('Content-Type', 'application/json; charset=utf-8')
    cron_update_json = urlopen(cron_update_request)

if __name__ == "__main__":
    lambda_handler()