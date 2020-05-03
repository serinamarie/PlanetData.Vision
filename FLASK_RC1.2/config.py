from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration variables from .env file."""

    # General Flask Config
    TESTING = environ.get('TESTING')
    DEBUG = environ.get('DEBUG')
    FLASK_APP = 'wsgi.py'
    FLASK_DEBUG = 1
    SECRETKEY = environ.get('SECRETKEY')

    # Database
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:hf3Ap24Hlseruxh84j3rw89@database-earth.cftcdswr9dvc.us-east-2.rds.amazonaws.com/"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
