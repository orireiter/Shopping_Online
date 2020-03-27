import pymongo
from pymongo import MongoClient


global client
client = MongoClient()

def db_info():
    db = client['COLBO_DB_TEST']

    collection = db['users']
    
    return collection

def register(username, password, email, tel):

    collection = db_info()
    
    already_exists = collection.find_one({'name': str(username)})

    if already_exists != None:
        return False
    object1 = {
        'name': username,
        'password': password,
        'email': email,
        'tel': tel
    }

    collection.insert_one(object1)
    return True

def login(username, password):

    collection = db_info()

    db_user = collection.find_one( { 'name': str(username)} )

    if db_user == None:
        return False, None
    elif db_user['name'] != str(username) or db_user['password'] != str(password):    
        return False, None
    else:
        id = str(db_user['_id'])
        return True, id