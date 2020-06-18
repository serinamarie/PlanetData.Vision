import json


def lambda_handler(event, context):
    '''Bird quality function'''

    # read airquality.json
    with open('wide_bird.json', 'r') as f:
        doc = json.loads(f.read())
        return doc
