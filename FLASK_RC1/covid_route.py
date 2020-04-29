import requests
from models import Summary, db

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize database
db = SQLAlchemy()


class Summary(db.Model):
    '''Attributes of summary API class'''
    slug = db.Column(db.String(100), primary_key=True)  # assigns this field
    country = db.Column(db.String(100), unique=True)
    countrycode = db.Column(db.String(100), unique=True)
    newconfirmed = db.Column(db.Integer)
    totalconfirmed = db.Column(db.Integer)
    newdeaths = db.Column(db.Integer)
    totaldeaths = db.Column(db.Integer)
    newrecovered = db.Column(db.Integer)
    totalrecovered = db.Column(db.Integer)
    date = db.Column(db.DateTime)
# def get_data():
#     '''Gets the data from the API, inserts into db'''
#     # request the data
#     response = requests.get("https://api.covid19api.com/summary")
#     nested_dict = response.json()
#     # Just get country data
#     record_list = nested_dict['Countries']
#     for record in record_list:
#         # get existing record from the db or initialize a new one
#         db_record = Summary.query.get(record['Slug']) or Summary(slug=record['Slug'])
#         # set its attributes
#         db_record.total_confirmed = record['TotalConfirmed']
#         # add/update record in db
#         db.session.add(db_record)
#     # commit changes
#     db.session.commit()
#     return record_list


def get_data():
    '''Gets the data from the API, inserts into db'''
    # request the data
    response = requests.get("https://api.covid19api.com/summary")
    nested_dict = response.json()
    # Just get country data
    record_list = nested_dict['Countries']
    for record in record_list:
        # get existing record from the db
        db_record = Summary.query.filter_by(slug=record['Slug']).first()
        # update all records
        db_record.newconfirmed = record['NewConfirmed']
        db_record.totalconfirmed = record['TotalConfirmed']
        db_record.newdeaths = record['NewDeaths']
        db_record.totaldeaths = record['TotalDeaths']
        db_record.newrecovered = record['NewRecovered']
        db.totalrecovered = record['TotalRecovered']
        db_record.date = record['Date']
        # add the record to the session
        db.session.add(db_record)
    # commit changes
    db.session.commit()
    return record_list
