from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def create_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes
        db.create_all()  # Create database tables for our data models
        db.session.commit()
        ma.init_app(app)

        return app
#
#
# def create_app():
#
#     app = Flask(__name__)
#     app.config.from_object('config.Config')
#
#     db.init_app(app)
#     ma.init_app(app)
#     return app
