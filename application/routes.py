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

# HOME DONE final
@app.route("/")
def index():
    '''Homepage endpoint to test whether app is working'''
    return render_template("index.html")

# SUMMARY/BUBBLES VIS DONE
@app.route("/bubbles/visual")
def bubbles():
    '''Returns the bubble visual and a brief intro to a tutorial'''
    return render_template('bubbles.html')

# SUMMARY/BUBBLES PULL DONE
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

# COUNTIES/USLIVE/HEATMAP PULL ROUTE 3500/day DONE
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

    # not_in_db = USCounties.query.filter_by(record['Date'] >= filter_after).first()
    # if not_in_db:
    #     print(not_in_db)
    #         new_record = USCounties(
    #             country=record['Country'],
    #             countrycode=record['CountryCode'],
    #             province=record['Province'],
    #             city=record['City'],
    #             citycode=record['CityCode'],
    #             lat=record['Lat'],
    #             lon=record['Lon'],
    #             cases=record['Cases'],
    #             status=record['Status'],
    #             date=record['Date'])
    #         db.session.add(new_record)
    #     else:
    #         pass
    # db.session.commit()
    return '200'
    # date = record['Date']
    # citycode = record['CityCode']
    # existing_record = USCounties.query.filter(
    #     USCounties.citycode == citycode, USCounties.date == date).first()
    #     if existing_record:
    #         pass
    #     if existing_record is None:
    #         new_record = USCounties(
    #             country=record['Country'],
    #             countrycode=record['CountryCode'],
    #             province=record['Province'],
    #             city=record['City'],
    #             citycode=record['CityCode'],
    #             lat=record['Lat'],
    #             lon=record['Lon'],
    #             cases=record['Cases'],
    #             status=record['Status'],
    #             date=record['Date'])  #
    #         db.session.add(new_record)  # Adds new User record to database
    # db.session.commit()  # Commits all changes
    # today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    return f'uscounties table for race chart vis in DB is up-to-date with covid summary API as of {today}'

    # iterate through each dictionary
    # for record in record_list:
    #     # filter out records that already exist
    #     try:
    #         db_record = USCounties.query.filter_by(date=record['Date']).first()
    #     # otherwise, add new records
    #     except NoResultFound:
    #         db_record = USCounties()
    #         db_record.country = record['Country']
    #         db_record.countrycode = record['CountryCode']
    #         db_record.state = record['Province']
    #         db_record.citycode = record['CityCode']
    #         db_record.lat = record['Lat']
    #         db_record.lon = record['Lon']
    #         db_record.cases = record['Cases']
    #         db_record.status = record['Status']
    #         db_record.date = record['Date']
    #     # add the record to the session
    #         db.session.add(db_record)
    # # commit changes
    # db.session.commit()
    # return record_list
    print(record_list)
    return '200'


# COUNTIES/COVIDALL/RACECHART PULL ROUTE
@app.route("/racechart/pull")
@app.route('/summary/pull')
def create_user():
    # """Create a user."""
    # response = requests.get("https://api.covid19api.com/summary",
    #                         headers={"User-Agent": "Mozilla Firefox/75.0"})
    # nested_dict = response.json()
    # # Just get country data
    # # record_list = nested_dict['Countries']
    record_list = [{"Country": "Algeria", "CountryCode": "DZ", "Slug": "algeria", "NewConfirmed": 199, "TotalConfirmed": 3848,
                    "NewDeaths": 7, "TotalDeaths": 444, "NewRecovered": 51, "TotalRecovered": 1702, "Date": "2020-04-30T23:49:34Z"}, {"Country": "American Samoa", "CountryCode": "AS", "Slug": "american-samoa", "NewConfirmed": 0, "TotalConfirmed": 0, "NewDeaths": 0, "TotalDeaths": 0, "NewRecovered": 0, "TotalRecovered": 0, "Date": "2020-04-30T23:49:34Z"}]
    for record in record_list:
        date = record['Date']
        country = record['Country']
        existing_record = Summary.query.filter(
            Summary.country == country, Summary.date == date).first()
        if existing_record:
            pass
        if existing_record is None:
            new_record = Summary(
                country=record['Country'],
                countrycode=record['CountryCode'],
                slug=record['Slug'],
                newconfirmed=record['NewConfirmed'],
                totalconfirmed=record['TotalConfirmed'],
                newdeaths=record['NewDeaths'],
                totaldeaths=record['TotalDeaths'],
                newrecovered=record['NewRecovered'],
                totalrecovered=record['TotalRecovered'],
                date=record['Date'])  #
            db.session.add(new_record)  # Adds new User record to database
    db.session.commit()  # Commits all changes
    return make_response('summary Data updated', 200)


# @app.route("/covidall/pull")
# def covidallpull():
#     '''Visiting this endpoint updates the db with fresher data from the all
#     COVID API'''
#     get_covidall_data()
#     today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
#     return f"New records added to DB as of {today}"


# class CovidAllSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = CovidAll
#
#
# covidallschema = CovidAllSchema(many=True)


@app.route('/covidall/pull/temp')
def get_covidall_data():
    '''Gets the data from the 'all' API for barchart race visual,
    inserts into db'''
    # request the data
    response = requests.get("https://api.covid19api.com/all")
    record_list = response.json()
    # if not json_input:
    #     return {"message": "No input data provided"}, 400
    # # validate and serialize the json
    # try:
    #     data = covidallschema.loads(json_input)
    # except ValidationError as err:
    #     return err.messages, 422
    # print(len(data), len(json_input), type(json_input))

    for data in record_list:
        # date_exists = CovidAll.query.filter_by(date=record['Date']).first()
        # print(date_exists, "Date already exists")
        #     if date_exists is None:
        #         # Creat new
        db_record = CovidAll(
            country=data['Country'],
            countrycode=data['CountryCode'],
            province=data['Province'],
            city=data['City'],
            citycode=data['CityCode'],
            lat=data['Lat'],
            lon=data['Lon'],
            confirmed=data['Confirmed'],
            deaths=data['Deaths'],
            recovered=data['Recovered'],
            active=data['Active'],
            date=data['Date']
        )
        return db_record
    #         db.session.add(db_record)
    # db.session.commit()
    # results = covidallschema.dump(record)
    # print(len(results))
    # return results, 201


@app.route('/covidall/json')
def get_covidall_json():
    '''Visiting this endpoint displays the covidall table from the db as a json
    endpoint for web to use for'''
    records = CovidAll.query.all()
    # Serialize the queryset
    results = covidallschema.dump(records)
    return results, 201


@app.route("/uscounties/pull")
def uscountiespull():
    '''Visiting this endpoint updates the db with fresher data from the US
    counties COVID API and displays them as a JSON endpoint for web to use for
    the heatmap visualization, began at 4:20'''
    return jsonify(get_uscounties_data())


# @app.route("/data")
# def data():
#     '''Visiting this endpoint updates the db with fresher data from the summary
#     API, then retrieves json from db and writes it to a json file'''
#     # creates a file called summary.json
#     # writeFile = open('summary.json', 'w')
#     # # writes to or replaces summary.json
#     # data = get_data()
#     # writeFile.write(json.dumps(data))
#     # # closes the file
#     # writeFile.close()
#     # return make_response("COVID Summary API freshly pulled into DB and summary.json")
#     return jsonify(get_data())
if __name__ == "__main__":
    app.run(debug=True)
