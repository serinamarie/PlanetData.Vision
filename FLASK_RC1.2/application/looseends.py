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
