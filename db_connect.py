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

def main():
    
    collection = db_info()

    # checking for seacrh bar use later on
    filter={ 'item name': { '$regex': 'קוקוס *' } }
    
    # can be add as an argument filter=filter
    # but right now finds all becasue {}
    # use skip and limit to decide which objects to show
    results = collection.find(filter=filter, limit=2)
    
    # need to loop through if there are multiple results
    for result in results:
        print("result name: ", result['item name'] )

    print("num of results: ", results.count())