import pymongo
from pymongo import MongoClient


global client
client = MongoClient()

def db_info():
    db = client['COLBO_DB_TEST']

    collection = db['users']
    
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