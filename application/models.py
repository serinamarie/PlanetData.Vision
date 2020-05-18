from flask_sqlalchemy import SQLAlchemy
from . import db, ma

# SUMMARY/BUBBLES CLASS


class Summary(db.Model):
    '''Attributes of '/summary' API class'''
    __tablename__ = 'summary'
    __table_args__ = {'extend_existing': True}
    country = db.Column(db.String(100), primary_key=True)
    totalconfirmed = db.Column(db.Integer)
    date = db.Column(db.DateTime)


class SummarySchema(ma.SQLAlchemyAutoSchema):
    '''
    Defunct as of 5/15/2020: Creates a Marshmallow schema for the Summary class
    to easily query the 'summary' table in the Postgres database. May need
    later.'''
    class Meta:
        model = Summary


# Set to many to allow filtering multiple queries
summary_schema = SummarySchema(many=True)

# COUNTIES/USLIVESTATUS/HEATMAP CLASS


class USCounties(db.Model):
    '''Attributes of US counties API class'''
    __tablename__ = 'uscounties'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    countrycode = db.Column(db.String(100))
    province = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(200), nullable=True)
    citycode = db.Column(db.String(5), nullable=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    cases = db.Column(db.Integer)
    status = db.Column(db.String(200))
    date = db.Column(db.DateTime(200))


class USCountiesSchema(ma.SQLAlchemyAutoSchema):
    '''
    Defunct as of 5/15/2020: Creates a Marshmallow schema for the USCounties
    class to easily query the 'uscounties' table in the Postgres database.
    May need later.'''
    class Meta:
        model = USCounties


# Set to many to allow filtering multiple queries
us_counties_schema = USCountiesSchema(many=True)

# COVID ALL/RACE CHART CLASS


class CovidAll(db.Model):
    '''Attributes of the '/all' Covid API class'''
    __tablename__ = 'covidall'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    countrycode = db.Column(db.String(100))
    province = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(200), nullable=True)
    citycode = db.Column(db.String(200), nullable=True)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    confirmed = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    recovered = db.Column(db.Integer)
    active = db.Column(db.Integer)
    date = db.Column(db.DateTime)


class CovidAllSchema(ma.SQLAlchemyAutoSchema):
    '''
    Defunct as of 5/15/2020: Creates a Marshmallow schema for the CovidAll class
    to easily query the 'covidall' table in the Postgres database. May need
    later.'''
    class Meta:
        model = CovidAll


# Set to many to allow filtering multiple queries
covidall_schema = CovidAllSchema(many=True)
