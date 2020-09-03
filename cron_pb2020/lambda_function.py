import json
from urllib.request import urlopen

def lambda_handler(event=None, context=None):
    '''
    Lambda function that gets data from the 2020PB api
    and sends it to a designated endpoint from ds api
    '''
    # requests pb2020 api
    content = urlopen('https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations.json').read().decode('utf-8')
    data = json.loads(content)
    print(data)

if __name__ == "__main__":
    lambda_handler()