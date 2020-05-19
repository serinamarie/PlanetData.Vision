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
import psycopg2
from sqlalchemy import text


api = Api(app)
ns_conf = api.namespace(
    'covid',
    description='Operations pertaining to the covid topic. None of these endpoints need to be visited as they are accessed only by AWS Lambda functions, or already exist as Lambda functions themselves. The ones that already exist as Lambda functions will eventually be deleted as they are superfluous.')


@ns_conf.route("/visual/summary")
class BubbleVisual(Resource):
    def get(self):
        '''Returns the D3 bubble visualization (best visited directly)
        through planetdata.world'''
        return render_template('bubbles.html')


@ns_conf.route("/summary")
class SummaryPull(Resource):
    def post(self):
        '''
        REPLACED: This endpoint pulls data from covid/summary API into database.
        Packaged as an AWS Lambda function. Accessible through API Gateway and
        uses CloudWatch to run once a day'''
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

    def get(self):
        '''REPLACED: This endpoint will filter and return all existing data from
        the 'summary' table in the database. It is no longer necessary as the
        AWS API Gateway endpoint does the same thing.'''
        all_records = Summary.query.all()
        # Replace SQLAlchemy with basic SQL magic
        result = summary_schema.dump(all_records)
        return jsonify(result)


@ns_conf.route("/uscounties")
class USCountiesPull(Resource):
    def post(self, days):
        '''
        A Heroku endpoint existing to be triggered by an AWS Lambda function
        each day via CloudWatch. There should never be a need to visit this
        endpoint yourself as it is automated to parse new data from the
        covid/live API into the AWS RDS PostgreSQL.'''

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
        '''Returns filtered data from the 'uscounties' table.'''

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


@ns_conf.route("/covidall")
class CovidAllPull(Resource):
    def post(self, days):
        '''
        A Heroku endpoint existing to be triggered by an AWS Lambda function
        each day via CloudWatch. There should never be a need to visit this
        endpoint yourself as it is automated to parse new data from the
        covid/all API into the AWS RDS PostgreSQL.'''

        # Request the data from external API
        covid_all_data = "https://api.covid19api.com/all"
        response = requests.get(covid_all_data)
        record_list = response.json()

        # Get new data (from today)
        todays_date = datetime.now().date()

        for record in record_list:

            # todays_date and record['date'] must have same format
            record['Date'] = datetime.strptime(record['Date'], '%Y-%m-%dT%H:%M:%SZ')

            if record['Date'] == todays_date:

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
        return f'DB is up-to-date with covid all API as of {todays_date}'

    def get(self):
        '''REPLACED: This endpoint will filter and return all existing data from
        the 'covidall' table in the database. It is no longer necessary as the
        AWS API Gateway endpoint does the same thing.'''

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

        rows = db.engine.execute(query)

        # Just post data necessary for the visualization
        covidall_dict = [
            {
                "country": row[0],
                "date": datetime.strptime(row[1], '%m-%d-%y').strftime('%Y/%m/%d'),
                "deaths": row[2]
            } for row in rows
        ]
        return jsonify(covidall_dict)


if __name__ == "__main__":
    app.run(debug=True)
