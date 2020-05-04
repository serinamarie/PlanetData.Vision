from .models import *
import requests
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
from flask_restplus import Api, Resource
import requests
from datetime import datetime, timedelta
import json

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
    def get(self):
        '''Returns all existing data from the 'summary' table in the database'''
        all_records = Summary.query.all()
        result = summary_schema.dump(all_records)
        return jsonify(result)

    def post(self):
        '''Gets data from the summary API for the bubbles visualization and
        inserts it into the database.'''
        summary_data = "https://api.covid19api.com/summary"
        # Request the data
        response = requests.get(summary_data)
        nested_dict = response.json()
        if not nested_dict:
            return {"message": "No input data provided"}, 400

            # Just get country data
            record_list = nested_dict['Countries']

            for record in record_list:

                # Get existing record from the db
                db_record = Summary.query.filter_by(slug=record['Slug']).first()

                # Update all records
                db_record.country = record['Country']
                db_record.countrycode = record['CountryCode']
                db_record.slug = record['Slug']
                db_record.newconfirmed = record['NewConfirmed']
                db_record.totalconfirmed = record['TotalConfirmed']
                db_record.newdeaths = record['NewDeaths']
                db_record.totaldeaths = record['TotalDeaths']
                db_record.newrecovered = record['NewRecovered']
                db_record.totalrecovered = record['TotalRecovered']
                db_record.date = record['Date']

                # Add the record to the session
                db.session.add(db_record)

                # Commit changes
                db.session.commit()

        # Return statement of verification
        this_moment = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        return f'DB is up-to-date with covid summary API as of {this_moment}'


@ns_conf.route("/uscounties/<days>")
class USCountiesPull(Resource):
    def post(self, days):
        '''
        Pulls data from web API into database.

        CAUTION: DO NOT PULL WITHOUT DISCUSSION
        Ex. of the 'days' parameter:
        If today is 5/2 and the last data pulled was from 4/28, choose 4 for
        days to add 5/2, 5/1, 4/30, and 4/29 to the database.

        This method will eventually be replaced with AWS Lambda, thank God.
        Meanwhile each date consists of 3500 records (350,000 records now and
        counting), so pull gently.'''

        # Request the data
        us_counties_data = "https://api.covid19api.com/country/us/status/confirmed/live"
        response = requests.get(us_counties_data)
        record_list = response.json()
        if not record_list:
            return {"message": "No input data provided"}, 400

            # Cast the 'days since last pulled' into a timestamp
            filter_after = datetime.today() - timedelta(int(days))

        for record in record_list:

            # Cast the json str of the record date to a datetime
            record['Date'] = datetime.strptime(record['Date'], '%Y-%m-%dT%H:%M:%SZ')

            # Take in a json string and creates a new record for it
            if record['Date'] >= filter_after:
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
        this_moment = datetime.today().strftime('%Y-%m-%d')
        return f'DB is up-to-date with covid summary API as of {this_moment} and has incorporated data since {days} days ago, including today if records have been posted for today'


@ns_conf.route("/uscounties")
class USCountiesDB(Resource):
    def get(self):
        '''Returns all existing data from the 'uscounties' table in the database'''
        all_records = USCounties.query.all()
        result = us_counties_schema.dump(all_records)
        return jsonify(result)


@ns_conf.route("/covidall/<days>")
class CovidAllPull(Resource):
    def post(self, days):
        '''
        Pulls data from web API into database.

        CAUTION: DO NOT PULL WITHOUT DISCUSSION
        Ex. of the 'days' parameter:
        If today is 5/2 and the last data pulled was from 4/28, choose 4 for
        days to add 5/2, 5/1, 4/30, and 4/29 to the database.

        This method will eventually be replaced with AWS Lambda, thank God.

        Meanwhile each date consists of 3500 records (350,000 records now and
        counting), so pull gently.'''

        # Request the data
        covid_all_data = "https://api.covid19api.com/all"
        response = requests.get(covid_all_data)
        record_list = response.json()
        if not record_list:
            return {"message": "No input data provided"}, 400

        # Cast the 'days since last pulled' into a timestamp
        filter_after = datetime.today() - timedelta(int(days))

        for record in record_list:

            # Cast the json str of the record date to a datetime
            record['Date'] = datetime.strptime(record['Date'], '%Y-%m-%dT%H:%M:%SZ')

            # Take in a json string and creates a new record for it
            if record['Date'] >= filter_after:
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
        this_moment = datetime.today().strftime('%Y-%m-%d')
        return f'DB is up-to-date with covid summary API as of {this_moment} and has incorporated data since {days} days ago, including today if records have been posted for today'


@ns_conf.route("/covidall")
class CovidAllDB(Resource):
    def get(self):
        '''Returns all existing data from the 'covidall' table in the database'''
        all_records = CovidAll.query.all()
        result = covidall_schema.dump(all_records)
        return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
