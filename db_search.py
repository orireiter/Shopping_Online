import pymongo
from pymongo import MongoClient


global client
client = MongoClient()

def db_info():
    db_list = client.list_database_names()
    # print("DB's: ", db_list)

    db_name = db_list[0]
    print("DB name: ", db_name, "\n")

    db = client[db_name]

    collection_list = db.list_collection_names()
    # print("Collections: ", collection_list)

    collection_name = collection_list[0]
    print("test collection: ", collection_name, "\n")

    collection = db[collection_name]
    
    return collection

def search(query):
    collection = db_info()

    empty_query_check = query.count(" ")
    
    '''print("spaces ", empty_query_check)
    print("query len ", len(query))'''

    if query == "" or empty_query_check == len(query):
        klum = "klum"
        return klum
    else:
        search_filter= { 'Name': { '$regex': str(query)+' *' } }
        search_list = collection.find(filter=search_filter)

    return search_list