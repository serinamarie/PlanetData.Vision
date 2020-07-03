import json


def lambda_handler(event, context):
    '''Air quality function 2'''

    # read airquality.json
    with open('airQuality.json', 'r') as f:
        doc = json.loads(f.read())
        return doc
