import json


def lambda_handler(event, context):

    # read airquality.json
    with open('airQuality.json', 'r') as f:
        doc = json.loads(f.read())
        return doc
