from flask_sqlalchemy import SQLAlchemy
from . import db, ma


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
    to easily query the 'covidall' table in the Postgres database (currently
    unused)'''
    class Meta:
        model = CovidAll


# Set to many to allow filtering multiple queries
covidall_schema = CovidAllSchema(many=True)
