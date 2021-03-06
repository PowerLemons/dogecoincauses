from pymongo import MongoClient
from configparser import SafeConfigParser


# Configuration file settings
parser = SafeConfigParser()
parser.read('settings/dogecoin.cfg')


def load_causes(dogecoin_causes, mongo_host, mongo_port, mongo_db, mongo_collect):
    '''
    Load an array of causes and inserts it in a MongoDB collection
    '''
    # MongoDB connection parameters
    mongo_client = MongoClient(mongo_host, mongo_port)
    mongo_database = mongo_client[mongo_db]
    mongo_collection = mongo_database[mongo_collect]

    # Insert causes in collection
    [mongo_collection.insert_one(cause) for cause in dogecoin_causes]


if __name__ == '__main__':
    '''
    Main method
    '''
    dogecoin_causes = [{'name': 'First cause', 'cause_id': 'c00001', 'country': 'Spain', 'country_3166': 'es', 'description': 'ajkfljskfasf', 'raised_money': 57.12},
        {'name': 'Second cause', 'cause_id': 'c00002', 'country': 'Netherlands', 'country_3166': 'nl', 'description': 'fsdfsferq', 'raised_money': 411.99},
        {'name': 'Third cause', 'cause_id': 'c00003', 'country': 'Colombia', 'country_3166': 'co', 'description': 'fsdghh', 'raised_money': 34.21},
        {'name': 'Fourth cause', 'cause_id': 'c00004', 'country': 'Belgium', 'country_3166': 'be', 'description': 'qegsgsgag', 'raised_money': 140.98}]

    load_causes(dogecoin_causes, parser.get('mongo_settings', 'mongo_host'), int(parser.get('mongo_settings', 'mongo_port')), parser.get('mongo_settings', 'mongo_db'), parser.get('mongo_settings', 'mongo_collection'))