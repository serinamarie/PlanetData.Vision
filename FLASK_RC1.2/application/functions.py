import requests
from models import Summary, USCounties, CovidAll, db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime


def get_uscounties_data():
    '''Gets the data from the us counties API for heatmap vis, inserts into db'''
    # request the data
    response = requests.get("https://api.covid19api.com/country/us/status/confirmed/live")
    record_list = response.json()
    # iterate through each dictionary
    for record in record_list:
        # filter out records that already exist
        try:
            db_record = USCounties.query.filter_by(date=record['Date']).first()
        # otherwise, add new records
        except NoResultFound:
            db_record = USCounties()
            db_record.country = record['Country']
            db_record.countrycode = record['CountryCode']
            db_record.state = record['Province']
            db_record.citycode = record['CityCode']
            db_record.lat = record['Lat']
            db_record.lon = record['Lon']
            db_record.cases = record['Cases']
            db_record.status = record['Status']
            db_record.date = record['Date']
        # add the record to the session
            db.session.add(db_record)
    # commit changes
    db.session.commit()
    return record_list


# def get_covidall_data():
#     '''Gets the data from the 'all' API for barchart race visual,
#     inserts into db'''
#     # request the data
#     response = requests.get("https://api.covid19api.com/all")
#     record_list = response.json()
#     rl_length = len(record_list)
#     print(rl_length)
#     db_record_length = CovidAll.query.all().count()
#     print(db_record_length)
    # iterate through each dictionary
    # for record in record_list:
    #     # filter out records that already exist
    #     try:
    #         db_record = Summary.query.filter_by(date=record['Date']).first()
    #     # otherwise, add new records
    #     except NoResultFound:
    #         # instantiates a class that can have these attributes
    #         db_record = Summary()
    #         # each record from the covid API is set to a class instance and
    #         # given its own attribute values
    #         db_record.country = record['Country']
    #         db_record.countrycode = record['CountryCode']
    #         db_record.state = record['Province']
    #         db_record.citycode = record['CityCode']
    #         db_record.lat = record['Lat']
    #         db_record.lon = record['Lon']
    #         db_record.confirmed = record['Confirmed']
    #         db_record.deaths = record['Deaths']
    #         db_record.recovered = record['Recovered']
    #         db_record.active = record['Active']
    #         db_record.date = record['Date']
    #
    #         # add the record to the session
    #         db.session.add(db_record)
    #
    #     # commit changes
    # db.session.commit()


if __name__ == '__main__':
    get_covidall_data()
