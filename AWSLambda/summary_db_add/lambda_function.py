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
    '''Parses /summary API for new data, adds to database.'''

    summary_data = "https://api.covid19api.com/summary"
    # Request the data
    response = requests.get(summary_data)
    nested_dict = response.json()
    record_list = nested_dict['Countries']

    for record in record_list:

        with conn.cursor() as cur:
            sql = 'UPDATE summary SET date=%s, totalconfirmed=%s WHERE country=%s;'
            data = (record['Date'], record['TotalConfirmed'], record['Country'])
            cur.execute(sql, data)
            conn.commit()
    return 'status: 200'
