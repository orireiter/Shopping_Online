import pymongo
from pymongo import MongoClient


global client
client = MongoClient()

def db_info():
    
    db = client['COLBO_DB_TEST']

    
    collection = db['another']
    
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