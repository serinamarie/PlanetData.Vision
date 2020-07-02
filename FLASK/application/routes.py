from .models import *
import requests
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
from flask_restplus import Api, Resource
from datetime import datetime, timedelta, date
import json
import psycopg2

api = Api(app)
ns_conf = api.namespace(
    'covid',
    description='Operations pertaining to the covid topic.')


@ns_conf.route("/uscounties/query")
class USCountiesPull(Resource):
    def get(self):
        '''Filters the data from the 'uscounties' table and returns json'''

        query = '''SELECT lat, lon, cases::int, to_char(date, 'MM-dd-yy')
        AS date FROM uscounties
        WHERE EXISTS (SELECT lat, lon, cases, date WHERE cases > 0)
        ORDER BY date ASC'''

        rows_1 = db.engine.execute(query)

        # Create a dictionary of all cases
        cases_dict = [{"lat": row[0], "lon": row[1], "cases": row[2], "date": row[3]}
                      for row in rows_1]

        rows_2 = db.engine.execute(query)

        # Create a list of all dates in records
        date_list = []
        for row in rows_2:
            date_list.append(row[3])

        # Concatenate the two objects into a dictionary
        records_dict = {
            'cases': cases_dict,
            # Unique, ordered dates only
            'dates': sorted(set(date_list))}
        return jsonify(records_dict)


if __name__ == "__main__":
    app.run(debug=True)
