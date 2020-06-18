from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api
from flask_compress import Compress
from flask_cors import CORS, cross_origin

# Instantiate relevant classes
db = SQLAlchemy()
ma = Marshmallow()
compress = Compress()


def create_app():
    '''Define how our app will operate'''

    # Initialize app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    CORS(app)

    # Initialize SQLAlchemy
    db.init_app(app)

    with app.app_context():

        # Import routes.py
        from . import routes

        # Create database tables for our data models
        db.create_all()

        # Commit all updates to database
        db.session.commit()

        # Initialize marshmallow
        ma.init_app(app)

        # Initialize compression capabilities
        compress.init_app(app)

        return app
