import sys
import logging
import psycopg2
import os
from datetime import datetime
import json

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

    # Grab the necessary results for the visualization and post to endpoint

    query = '''SELECT lat, lon, cases::int, to_char(date, 'MM-dd-yy')
    AS date FROM uscounties
    WHERE EXISTS (SELECT lat, lon, cases, date WHERE cases > 0)
    ORDER BY date ASC'''

    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
        rows_1 = cur.fetchall()
        rows_2 = rows_1.copy()

    # Create a dictionary of all cases
    cases_dict = [{"lat": row[0], "lon": row[1], "cases": row[2], "date": row[3]} for row in rows_1]

    # Create a list of all dates in records
    date_list = []
    for row in rows_2:
        date_list.append(row[3])

    # Concatenate the two objects into a dictionary
    records_dict = {
        'cases': cases_dict,
        # Unique, ordered dates only
        'dates': sorted(set(date_list))}
    return json.dumps(records_dict)
