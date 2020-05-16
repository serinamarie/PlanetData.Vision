from .models import *
import requests
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
from flask_restplus import Api, Resource
import requests
from datetime import datetime, timedelta
import json
from math import ceil

api = Api(app)
ns_conf = api.namespace(
    'covid',
    description='Operations pertaining to the covid topic')


@ns_conf.route("/visual/summary")
class BubbleVisual(Resource):
    def get(self):
        '''Returns the D3 bubble visualization (best visited directly)'''
        return render_template('bubbles.html')


@ns_conf.route("/summary")
class SummaryPull(Resource):
    def post(self):
        '''Returns all existing data from the 'summary_be' table in the
        database, filters it, and inserts it into summary_fe. This endpoint
        should be triggered by new data entering the summary_be table'''
        all_records = Summary.query.all()
        # Replace SQLAlchemy with basic SQL magic
        result = summary_schema.dump(all_records)
        return jsonify(result)

    def get(self):
        '''
        Pulls data from covid/summary API into database.
        Uses API Gateway, AWS Lambda and CloudWatch to run once a day'''
        summary_data = "https://api.covid19api.com/summary"
        # Request the data
        response = requests.get(summary_data)
        nested_dict = response.json()

        # Just get country data
        record_list = nested_dict['Countries']

        for record in record_list:

            # Get existing record from the db
            db_record = Summary.query.get(record['Country']) or Summary(country=record['Country'])
            # Update all records
            db_record.totalconfirmed = record['TotalConfirmed']
            db_record.date = record['Date']
            # Add the record to the session
            db.session.add(db_record)

        # Commit changes
        db.session.commit()

        # Return statement of verification
        return 'status: 200'


@ns_conf.route("/uscounties")
class USCountiesPull(Resource):
    def get(self, days):
        '''
        Pulls data from covid/live API into database.
        Will use API Gateway, AWS Lambda and CloudWatch to run each day'''

        # Request the data
        us_counties_data = "https://api.covid19api.com/country/us/status/confirmed/live"
        response = requests.get(us_counties_data)
        record_list = response.json()

        # Get new data (from today)
        todays_data = datetime.now().date()

        for record in record_list:

            # Cast the json str of the record date to a datetime
            record['Date'] = datetime.strptime(record['Date'], '%Y-%m-%dT%H:%M:%SZ')

            # Take in a json string and creates a new record for it
            if record['Date'] == todays_data:
                new_record = USCounties(
                    country=record['Country'],
                    countrycode=record['CountryCode'],
                    province=record['Province'],
                    city=record['City'],
                    citycode=record['CityCode'],
                    lat=record['Lat'],
                    lon=record['Lon'],
                    cases=record['Cases'],
                    status=record['Status'],
                    date=record['Date'])

                # Add record to database
                db.session.add(new_record)
            else:
                pass

        # Commit all records to database
        db.session.commit()

        # Return statement of verification
        return f'DB is up-to-date with covid all API as of {todays_data}'

    def get(self):
        '''Returns all existing data from the 'uscounties_be' table in the
        database, filters it, and inserts it into uscounties_fe. This endpoint
        should be triggered by new data entering the uscounties_be table'''
        all_records = USCounties.query.all()
        # Replace SQLAlchemy with basic SQL magic
        result = us_counties_schema.dump(all_records)
        return jsonify(result)


@ns_conf.route("/covidall")
class CovidAllPull(Resource):
    def get(self, days):
        '''
        Pulls data from covid/all API into database.
        Will use API Gateway, AWS Lambda and CloudWatch to run each day'''

        # Request the data
        covid_all_data = "https://api.covid19api.com/all"
        response = requests.get(covid_all_data)
        record_list = response.json()

        # Get new data (from today)
        todays_data = datetime.now().date()

        for record in record_list:

            # Cast the json str of the record date to a datetime to compare to today's date
            record['Date'] = datetime.strptime(record['Date'], '%Y-%m-%dT%H:%M:%SZ')

            # Take in a json string and creates a new record for it
            if record['Date'] == todays_data:
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
        return f'DB is up-to-date with covid all API as of {todays_data}'

    def post(self):
        '''Returns all existing data from the 'covidall_be' table in the
        database, filters it, and inserts it into to covidall_fe. This endpoint
        should be triggered by new data entering the covidall_be table'''
        all_records = CovidAll.query.all()
        # Replace SQLAlchemy with basic SQL magic
        result = covidall_schema.dump(all_records)
        return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
