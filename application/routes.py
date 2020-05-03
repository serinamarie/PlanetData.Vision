from .models import db, Summary, USCounties
import requests
from flask import Flask, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import psycopg2
import requests
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timedelta
from flask import current_app as app
import json


@app.route("/")
def index():
    '''Homepage endpoint to test whether app is working'''
    return render_template("index.html")


@app.route("/bubbles/visual")
def bubbles():
    '''Returns the bubble visual and a brief intro to a tutorial'''
    return render_template('bubbles.html')


@app.route("/bubbles/pull")
def get_summary_data(ACCESS):
    '''Gets the data from the summary API for the bubbles visualization and
    inserts it into the database.'''

    # Request the data
    response = requests.get("https://api.covid19api.com/summary")
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
    today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    return f'DB is up-to-date with covid summary API as of {today}'


@app.route("/heatmap/pull/<dayssincelastpulled>")
def get_uscounties_data(dayssincelastpulled):
    '''
    Gets the data from the us counties API for the heatmap visualization and
    inserts it into the database.

    Ex. of the 'dayssincelastpulled' parameter:
    If today is 5/2 and the last data pulled was from 4/28, choose 4 for
    dayssincelastpulled to add 5/2, 5/1, 4/30, and 4/29 to the database.

    This methods will eventually be replaced with AWS Lambda.'''

    # Request the data
    us_counties_data = "https://api.covid19api.com/country/us/status/confirmed/live"
    response = requests.get(us_counties_data)
    record_list = response.json()
    if not record_list:
        return {"message": "No input data provided"}, 400

    # Cast the 'days since last pulled' into a timestamp
    filter_after = datetime.today() - timedelta(int(dayssincelastpulled))

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
    today = datetime.today().strftime('%Y-%m-%d')
    return f'DB is up-to-date with covid summary API as of {today} and has incorporated data since {filter_after}'


# COUNTIES/COVIDALL/RACECHART PULL ROUTE
@app.route("/racechart/pull")
def function():
    return 'to finish this task on 5/3/20'


if __name__ == "__main__":
    app.run(debug=True)
