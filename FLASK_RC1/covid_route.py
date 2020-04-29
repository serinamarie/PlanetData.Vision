import requests
from models import Summary, db


def get_data():
    '''Gets the data from the API, inserts into db'''
    # request the data
    response = requests.get("https://api.covid19api.com/summary")
    nested_dict = response.json()
    # Just get country data
    record_list = nested_dict['Countries']
    for record in record_list:
        # get existing record from the db or initialize a new one
        db_record = Summary.query.get(record['Slug']) or Summary(slug=record['Slug'])
        # set its attributes
        db_record.total_confirmed = record['TotalConfirmed']
        db_record.country = record['Country']
        # add/update record in db
        db.session.add(db_record)
    # commit changes
    db.session.commit()
    return record_list
