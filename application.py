import json
import flask
from pymongo import MongoClient
from flask import request, make_response
from configparser import SafeConfigParser


__version__ = '0.1.1'
__status__ = 'Development'


application = flask.Flask(__name__)


# Configuration file settings
parser = SafeConfigParser()
parser.read('settings/dogecoin.cfg')


@application.route('/causes')
def causes_forecast():
    '''
    Process causes request
    '''
    # MongoDB connection parameters
    mongo_client = MongoClient(parser.get('mongo_settings', 'mongo_host'), int(parser.get('mongo_settings', 'mongo_port')))
    mongo_database = mongo_client[parser.get('mongo_settings', 'mongo_db')]
    mongo_collection = mongo_database[parser.get('mongo_settings', 'mongo_collection')]
    mongo_cursor = mongo_collection.find({})

    # Create and populate JSON data structure
    json_dict = {}
    json_dict['causes'] = [format_cause_json(cause) for cause in mongo_cursor]

    # Create response body
    response = make_response(json.dumps(json_dict))
    response.mimetype = 'application/json'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = 0

    # Send response
    return response


def format_cause_json(mongo_cause):
    '''
    Formats cause dictionary (not useful at the moment, just parses attributes)
    '''
    cause_json = {}

    cause_json['desc'] = mongo_cause['description']
    cause_json['name'] = mongo_cause['name']
    cause_json['country'] = mongo_cause['country']
    cause_json['money'] = mongo_cause['raised_money']

    return cause_json


# Delete in EBS
application.run()