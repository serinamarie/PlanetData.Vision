import json


def lambda_handler(event, context):
    '''Deforestation predictions function'''

    # read airquality.json
    with open('Deforestation_Predictions.json', 'r') as f:
        doc = json.loads(f.read())
        return doc
