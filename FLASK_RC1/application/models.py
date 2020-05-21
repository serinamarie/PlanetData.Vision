from flask_sqlalchemy import SQLAlchemy
from . import db, ma

# Marshmallow is defunct within this app at the moment 5/20/20


class Summary(db.Model):
    '''Attributes of '/summary' API class for the bubbles vis'''
    __tablename__ = 'summary'
    __table_args__ = {'extend_existing': True}
    country = db.Column(db.String(100), primary_key=True)
    totalconfirmed = db.Column(db.Integer)
    date = db.Column(db.DateTime)


class SummarySchema(ma.SQLAlchemyAutoSchema):
    '''Creates a Marshmallow schema for the Summary class
    to easily query the 'summary' table in the Postgres database'''
    class Meta:
        model = Summary


# Set to many to allow filtering multiple queries
summary_schema = SummarySchema(many=True)


class USCounties(db.Model):
    '''Attributes of US counties API class for the heatmap'''
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
    '''Creates a Marshmallow schema for the USCounties
    class to easily query the 'uscounties' table in the Postgres database.'''
    class Meta:
        model = USCounties


# Set to many to allow filtering multiple queries
us_counties_schema = USCountiesSchema(many=True)


class CovidAll(db.Model):
    '''Attributes of the '/all' Covid API class for racechart vis'''
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
    '''Creates a Marshmallow schema for the CovidAll class
    to easily query the 'covidall' table in the Postgres database.'''
    class Meta:
        model = CovidAll


# Set to many to allow filtering multiple queries
covidall_schema = CovidAllSchema(many=True)
