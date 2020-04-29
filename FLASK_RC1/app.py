import requests
from flask import Flask, render_template, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import psycopg2
from models import Summary, USLive, db
from covid_route import get_data
import json


# get our environment variables
load_dotenv()

# Initialize application
app = Flask(__name__)

# assign our Postgres url
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/'.format(
    user=os.getenv("POSTGRES_USER"),
    pw=os.getenv("POSTGRES_PW"),
    url=os.getenv("POSTGRES_URL")
)

# Set up db
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# End complaints
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# assign home route
@app.route("/")
def index():
    '''Homepage endpoint to test whether app is working'''
    return render_template("index.html")


@app.route("/data")
def data():
    '''Visiting this endpoint updates the db with fresher data from the summary
    API, then retrieves json from db and writes it to a json file'''
    # creates a file called summary.json
    writeFile = open('summary.json', 'w')
    # writes to or replaces summary.json
    writeFile.write(json.dumps(get_data()))
    # closes the file
    writeFile.close()
    return make_response("COVID Summary API freshly pulled into DB and summary.json")


@app.route("/bubbles")
def bubbles():
    '''Returns the bubble visual and a brief intro to a tutorial'''
    return render_template('bubbles.html')


if __name__ == "__main__":
    app.run(debug=True)
