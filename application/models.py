from flask_sqlalchemy import SQLAlchemy
from . import db

# SUMMARY/BUBBLES CLASS
class Summary(db.Model):
    '''Attributes of '/summary' API class'''
    __tablename__ = 'summary'
    __table_args__ = {'extend_existing': True}
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

#COUNTIES/USLIVE/HEATMAP PULL ROUTE
class USCounties(db.Model):
    '''Attributes of US counties API class'''
    __tablename__ = 'uscounties'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)  # assigns this field
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

# class Covid(db.Model):
#     '''Attributes of the '/all' Covid API class'''
#     __tablename__ = 'covid'
#     __table_args__ = {'extend_existing': False}
#     id = db.Column(db.Integer, primary_key=True)  # assigns this field
#     country = db.Column(db.String(100), unique=True)
#     countrycode = db.Column(db.String(100), unique=True)
#     state = db.Column(db.String(200))
#     province = db.Column(db.String(200))
#     citycode = db.Column(db.String(200))
#     lat = db.Column(db.Float)
#     lon = db.Column(db.Integer)
#     confirmed = db.Column(db.Integer)
#     deaths = db.Column(db.Integer)
#     recovered = db.Column(db.Integer)
#     active = db.Column(db.Integer)
#     date = db.Column(db.DateTime)
