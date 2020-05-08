import pymongo,configparser
from pymongo import MongoClient


global client
client = MongoClient()

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

def show_40(page_num):
    # getting collection
    collection = db_info()
    
    if int(page_num) < 1 or int(page_num) > 259:
        
        return "exception"
    
    else : 
        # setting counter by page number, need to set that in URL as well
        counter = ( (int(page_num)-1) * 40 )

        # queries 40 items with correlation to the page number
        get_40 = collection.find(filter=None, skip=counter, limit=40)

        return get_40