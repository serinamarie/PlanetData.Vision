import json


def lambda_handler(event, context):
    '''Globe data''

    # read airquality.json
    with open('globe_data_uncompressed.json', 'r') as f:
        doc = json.loads(f.read())
        return doc
