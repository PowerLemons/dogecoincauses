import json
import flask
from pymongo import MongoClient
from flask import request, make_response
from configparser import SafeConfigParser


__version__ = '0.2.0'
__status__ = 'Development'


application = flask.Flask(__name__)


# Configuration file settings
parser = SafeConfigParser()
parser.read('settings/dogecoin.cfg')


# Support functions
def is_number(string_value):
    try:
        float(string_value)
        return True
    except ValueError:
        return False
# /Support functions


@application.route('/causes')
def causes_forecast():
    '''
    Process causes request
    '''
    if ('filter' in request.args):
        filter_name = request.args['filter']

        # MongoDB connection parameters
        mongo_client = MongoClient(parser.get('mongo_settings', 'mongo_host'), int(parser.get('mongo_settings', 'mongo_port')))
        mongo_database = mongo_client[parser.get('mongo_settings', 'mongo_db')]
        mongo_collection = mongo_database[parser.get('mongo_settings', 'mongo_collection')]

        if (filter_name == 'all'):
            # Get all items of the collection
            mongo_cursor = mongo_collection.find({})

            # Create and populate JSON data structure
            json_dict = {}
            json_dict['causes'] = [format_cause_json(cause) for cause in mongo_cursor]

        elif (filter_name == 'money'):
            # Apply raised money filter
            json_dict = {}

            # Check input parameters and their integrity
            if ('from' in request.args) and ('to' in request.args) and (is_number(request.args['from'])) and (is_number(request.args['to'])):
                mongo_cursor = mongo_collection.aggregate([{'$match': {'raised_money': {'$gte': float(request.args['from']), '$lte': float(request.args['to'])}}}])

                # Populate JSON data structure
                json_dict['causes'] = [format_cause_json(cause) for cause in mongo_cursor]
            else:
                # Notify wrong filter parameters
                json_dict['error'] = 'wrong_money_filter_params'

        elif (filter_name == 'country_id'):
            # Apply country filter
            json_dict = {}

            # Check if country codes are sent
            if ('code' in request.args):
                # Generates a list of ISO 3166-1 compliant country codes 
                country_codes = request.args.getlist('code')

                mongo_cursor = mongo_collection.find({'country_3166': {'$in': country_codes}})

                # Populate JSON data structure
                json_dict['causes'] = [format_cause_json(cause) for cause in mongo_cursor]
            else:
                # Notify wrong filter parameters
                json_dict['error'] = 'no_country_codes'

        elif (filter_name == 'cause_id'):
            # Apply cause id filter
            json_dict = {}

            # Check if cause ids are sent
            if ('id' in request.args):
                # Generates a list of cause ids 
                cause_ids = request.args.getlist('id')

                mongo_cursor = mongo_collection.find({'cause_id': {'$in': cause_ids}})

                # Populate JSON data structure
                json_dict['causes'] = [format_cause_json(cause) for cause in mongo_cursor]
            else:
                # Notify wrong filter parameters
                json_dict['error'] = 'no_cause_ids'

        else:
            # Notify wrong filter
            json_dict = {}
            json_dict['error'] = 'wrong_filter'

        # Close MongoDB connection
        mongo_client.close()

    else:
        json_dict = {}
        json_dict['error'] = 'no_filter'

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

    cause_json['id'] = mongo_cause['cause_id']
    cause_json['desc'] = mongo_cause['description']
    cause_json['name'] = mongo_cause['name']
    cause_json['country'] = mongo_cause['country']
    cause_json['money'] = mongo_cause['raised_money']

    return cause_json


# Delete in EBS
application.run()