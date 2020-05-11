import pymongo, configparser
from pymongo import MongoClient


global client
client = MongoClient()

# searches db with regex to allow items containing to given word to show up ,
# better regex need to be set up

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

    collection = get_config("item_col")
    collection = db[collection]
    
    return collection

def search(query):
    collection = db_info()

    empty_query_check = query.count(" ")
    

    if query == "" or empty_query_check == len(query):
        klum = "klum"
        return klum
    else:
        search_filter= { 'Name': { '$regex': str(query)+' *' } }
        search_list = collection.find(filter=search_filter)

    return search_list