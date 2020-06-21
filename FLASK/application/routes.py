from .models import *
import requests
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
from flask_restplus import Api, Resource
import requests
from datetime import datetime, timedelta, date
import json
from math import ceil
import psycopg2
from sqlalchemy import text
from flask import render_template

api = Api(app)
ns_conf = api.namespace(
    'covid',
    description='Operations pertaining to the covid topic.')


@ns_conf.route("/uscounties/query")
class USCountiesPull(Resource):
    def get(self):
        '''Filters the data from the 'uscounties' table and returns json'''

        query = '''SELECT lat, lon, cases::int, to_char(date, 'MM-dd-yy')
        AS date FROM uscounties
        WHERE EXISTS (SELECT lat, lon, cases, date WHERE cases > 0)
        ORDER BY date ASC'''

        rows_1 = db.engine.execute(query)

        # Create a dictionary of all cases
        cases_dict = [{"lat": row[0], "lon": row[1], "cases": row[2], "date": row[3]}
                      for row in rows_1]

        rows_2 = db.engine.execute(query)

        # Create a list of all dates in records
        date_list = []
        for row in rows_2:
            date_list.append(row[3])

        # Concatenate the two objects into a dictionary
        records_dict = {
            'cases': cases_dict,
            # Unique, ordered dates only
            'dates': sorted(set(date_list))}
        return jsonify(records_dict)


@ns_conf.route("/covidall/add")
class CovidAllPull(Resource):
    def get(self):
        '''Parses new data from the covid/all API into the AWS RDS PostgreSQL.
        An AWS Lambda function calls this endpoint each day.'''

        # Request the data from external API
        covid_all_data = "https://api.covid19api.com/all"
        record_list = requests.get(covid_all_data).json()

        # Get new data (from today)
        todays_date = datetime.now().date()

        # Yesterday's date works better across timezones to ensure
        # no data will be missed
        yesterdays_date = todays_date - timedelta(1)

        for record in record_list:

            # format of the existing json date string
            format = '%Y-%m-%dT%H:%M:%SZ'

            # make the json record 'date' column a datetime object
            dt = datetime.strptime(record['Date'], format)

            # format it to match todays_date
            date_record = date(dt.year, dt.month, dt.day)

            if date_record == yesterdays_date:

                # Take in a json string and creates a new record for it
                new_record = CovidAll(
                    country=record['Country'],
                    countrycode=record['CountryCode'],
                    province=record['Province'],
                    city=record['City'],
                    citycode=record['CityCode'],
                    lat=record['Lat'],
                    lon=record['Lon'],
                    confirmed=record['Confirmed'],
                    deaths=record['Deaths'],
                    recovered=record['Recovered'],
                    active=record['Active'],
                    date=record['Date']
                )

                # Add record to database
                db.session.add(new_record)
            else:
                pass

            # Commit all records to database
            db.session.commit()

        # Return statement of verification
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps("Data for racechart refreshed!")
        }


if __name__ == "__main__":
    app.run(debug=True)
