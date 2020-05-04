from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api

db = SQLAlchemy()
ma = Marshmallow()


def create_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        # Import routes
        from . import routes
        # Create database tables for our data models
        db.create_all()
        # Commit all updates to database
        db.session.commit()
        ma.init_app(app)

        return app
