import sys
import logging
import psycopg2
import json
import os
import requests
from datetime import datetime, timedelta

# rds settings
rds_host = os.environ.get('RDS_HOST')
rds_username = os.environ.get('RDS_USERNAME')
rds_user_pwd = os.environ.get('RDS_USER_PWD')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn_string = "host=%s user=%s password=%s" % \
        (rds_host, rds_username, rds_user_pwd)
    conn = psycopg2.connect(conn_string)
except:
    logger.error("ERROR: Could not connect to Postgres instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS Postgres instance succeeded")


def lambda_handler(event, context):
    '''Parses covid/all API for new data, adds to database.'''

    covidall_add_endpoint = "https://ds-backend-planetdata.herokuapp.com/covid/covidall/add"
    # Request the data
    response = requests.get(covidall_add_endpoint)

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps("Racechart data updated!")
    }
