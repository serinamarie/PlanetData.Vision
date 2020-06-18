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
    description='Operations pertaining to the covid topic. Only the GET covid/uscounties endpoints need to be visited as they are accessed only by AWS Lambda functions, or already exist as Lambda functions themselves. The ones that already exist as Lambda functions will eventually be deleted as they are superfluous.')


# @ns_conf.route("/summary")
# class SummaryPull(Resource):
#     def post(self):
#         '''This endpoint pulls data from covid/summary API into database.
#         Accessible through API Gateway and uses CloudWatch to run once a day.
#         Defunct (AWS Lambda Function).'''
#
#         summary_data = "https://api.covid19api.com/summary"
#         # Request the data
#         response = requests.get(summary_data)
#         nested_dict = response.json()
#
#         # Just get country dictionary
#         record_list = nested_dict['Countries']
#
#         for record in record_list:
#
#             # Get existing record from the db
#             db_record = Summary.query.get(record['Country']) or Summary(country=record['Country'])
#
#             # Update record's # of confirmed as well as the date
#             db_record.totalconfirmed = record['TotalConfirmed']
#             db_record.date = record['Date']
#
#             # Add the record to the session
#             db.session.add(db_record)
#
#         # Commit changes
#         db.session.commit()
#
#         # Return statement of verification
#         return {
#             'statusCode': 200,
#             'headers': {'Content-Type': 'application/json'},
#             'body': json.dumps("Data for bubble vis refreshed!")
#         }
#
#     def get(self):
#         '''Returns all existing data from the 'summary' table in the database.
#         Defunct (AWS Lambda package).'''
#
#         # Return all data
#         query = """select * from summary"""
#         rows = db.engine.execute(query)
#
#         # Create the schema for front end
#         record_list = [
#             {
#                 'country': row[0],
#                 'totalconfirmed': row[1]
#             } for row in rows
#         ]
#
#         return jsonify(record_list)


# @ns_conf.route("/uscounties/add")
# class USCountiesPull(Resource):
# def get(self):
#     '''Parses new data from the covid/live API into the AWS
#     RDS PostgreSQL. An AWS Lambda function calls this endpoint each day.'''
#
#     # Request the data
#     us_counties_data = "https://api.covid19api.com/country/us/status/confirmed/live"
#     record_list = requests.get(us_counties_data).json()
#
#     # Get new data (from today only)
#     todays_date = datetime.now().date()
#
#     for record in record_list:
#
#         # format of the existing json date string
#         format = '%Y-%m-%dT%H:%M:%SZ'
#
#         # make the json record 'date' column a datetime object
#         dt = datetime.strptime(record['Date'], format)
#
#         # format it to match todays_date
#         record['Date'] = date(dt.year, dt.month, dt.day)
#
#         # Take in a json string and creates a new record for it
#         if record['Date'] == todays_date:
#             new_record = USCounties(
#                 country=record['Country'],
#                 countrycode=record['CountryCode'],
#                 province=record['Province'],
#                 city=record['City'],
#                 citycode=record['CityCode'],
#                 lat=record['Lat'],
#                 lon=record['Lon'],
#                 cases=record['Cases'],
#                 status=record['Status'],
#                 date=record['Date'])
#
#             # Add record to database
#             db.session.add(new_record)
#
#         # Commit all records to database
#         db.session.commit()
#
#     # Return statement of verification
#     return {
#         'statusCode': 200,
#         'headers': {'Content-Type': 'application/json'},
#         'body': json.dumps("Data for heatmap refreshed!")
#     }


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

        for record in record_list:

            # format of the existing json date string
            format = '%Y-%m-%dT%H:%M:%SZ'

            # make the json record 'date' column a datetime object
            dt = datetime.strptime(record['Date'], format)

            # format it to match todays_date
            record['Date'] = date(dt.year, dt.month, dt.day)

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
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps("Data for racechart refreshed!")
        }


# @ns_conf.route("/covidall/query")
# class CovidAllPull(Resource):
#     def get(self):
#         '''Filters and returns data from the 'covidall' table in the database
#         for the racechart visual. Defunct (AWS API Gateway & AWS Lambda).'''
#
#         query = '''
#         SELECT ranked_countries.country,
#         to_char(ranked_countries.date, 'MM-dd-yy'),
#         sum(ranked_countries.deaths) AS deaths
#         FROM(
#         SELECT covidall.country, covidall.date, covidall.deaths, rank()
#         OVER(PARTITION BY covidall.date ORDER BY covidall.deaths DESC)
#         FROM covidall WHERE province='' OR country='China') ranked_countries
#         WHERE rank <= 20 AND deaths > 0
#         GROUP BY ranked_countries.date, ranked_countries.country
#         ORDER BY ranked_countries.date'''
#         # ¯\_(ツ)_/¯
#
#         rows = db.engine.execute(query)
#
#         # Just post data necessary for the visualization
#         covidall_dict = [
#             {
#                 "country": row[0],
#                 "date": datetime.strptime(row[1], '%m-%d-%y').strftime('%Y/%m/%d'),
#                 "deaths": row[2]
#             } for row in rows
#         ]
#         return jsonify(covidall_dict)


if __name__ == "__main__":
    app.run(debug=True)
