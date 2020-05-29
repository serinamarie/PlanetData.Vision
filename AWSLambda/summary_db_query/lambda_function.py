import sys
import logging
import psycopg2
import json
import os

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

    records = []

    query = """select *
            from summary
            """

    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
        for row in cur:
            # Filter for countries with cases > 0 (should be all)
            if row[1] > 0:
                record = {
                    'country': row[0],
                    'totalconfirmed': row[1]
                }
                records.append(record)

    return records
