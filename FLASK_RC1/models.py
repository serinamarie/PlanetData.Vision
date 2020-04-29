from flask_sqlalchemy import SQLAlchemy

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


class USLive(db.Model):
    '''Attributes of us live API class'''
    id = db.Column(db.Integer, primary_key=True)  # assigns this field
    country = db.Column(db.String(100), unique=True)
    state = db.Column(db.String(200))
    lat = db.Column(db.Float)
    lon = db.Column(db.Integer)
    confirmed = db.Column(db.Integer)
    deaths = db.Column(db.Integer)
    recovered = db.Column(db.Integer)
    active = db.Column(db.Integer)
    date = db.Column(db.DateTime)
