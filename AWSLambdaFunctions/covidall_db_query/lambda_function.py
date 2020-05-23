import sys
import logging
import psycopg2
import os
from datetime import datetime

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

    query = '''
    SELECT ranked_countries.country,
    to_char(ranked_countries.date, 'MM-dd-yy'),
    sum(ranked_countries.deaths) AS deaths
    FROM (
    SELECT covidall.country, covidall.date, covidall.deaths, rank()
    OVER (PARTITION BY covidall.date ORDER BY covidall.deaths DESC)
    FROM covidall WHERE province = '' OR country = 'China') ranked_countries
    WHERE rank <=20 AND deaths > 0
    GROUP BY ranked_countries.date, ranked_countries.country
    ORDER BY ranked_countries.date'''

    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
        rows = cur.fetchall()

        covidall_dict = [
            {
                "country": row[0],
                "date": datetime.strptime(row[1], '%m-%d-%y').strftime('%Y/%m/%d'),
                "deaths": row[2]
            } for row in rows
        ]
    return covidall_dict
