import pymongo, configparser
from pymongo import MongoClient


global client
client = MongoClient()

# this pages checks id against username
# thats to make sure users didnt try to get through login
# its not really secure and needs to be changed

#------------------------------------------------------------------#
# PARSER related

# creating a parser for a config file for better use later on
# it takes as an argument to parameter youre looking for
# and retrieves the variable in it
def get_config(parameter):
    parser = configparser.RawConfigParser()
    config_path = r".\app.config"
    parser.read(config_path)
    return parser.get('app-config', str(parameter))

# -----------------------------------------------------------#

def db_info():
    db = get_config("db")
    db = client[db]

    collection = get_config("user_col")
    collection = db[collection]
    
    return collection

def url_check(username, id):

    collection = db_info()

    db_user = collection.find_one( { 'name': str(username)} )
    
    if db_user == None:
        return False
    
    id0 = str(db_user['_id'])
    if db_user['name'] != str(username) or id0 != str(id):    
        return False
    
    else:
        return True