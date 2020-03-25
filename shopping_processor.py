import json
import datetime
import os


#this need to run everytime the page loads so adding item will be okay
def load_order(username):
    order_name = str(username)+str(datetime.date.today())+".json"
    for files in os.walk(r".\orders\\"): 
        file_checker = files[2]
    
    if order_name in file_checker:
        
        order_file = open(r".\orders\\"+str(username)+str(datetime.date.today())+".json", "r")
        order_obj = order_file.read()
        order_json = json.loads(order_obj)
        key_list = list(order_json.keys())
        value_list = list(order_json.values())
        # need to make keys - name 
        # and values - amount
        
        order_file.close()
        return value_list, key_list
        # add return to get presentation of bag, also with username
    

    else:

        order_file = open(r".\orders\\"+str(username)+str(datetime.date.today())+".json", "w")
        order_file.write("{}")
        order_file.close()
        empty = "empty"
        


# load_order("ori")

def add_item(item, username):
    path = ".\orders\\"+str(username)+str(datetime.date.today())+".json"
    
    order_file = open(path, "r")
    
    order_obj = order_file.read()
    order_json = json.loads(order_obj)
    try:
        order_json[str(item)] = str(1 + int(order_json[str(item)]))
    except:
        order_json[str(item)] = str(1)
    order_file = open(r".\orders\\"+str(username)+str(datetime.date.today())+".json", "w")
    order_json = json.dumps(order_json)
    order_file.write(order_json)
    order_file.close()
        

def delete_item(item, username):
    path = ".\orders\\"+str(username)+str(datetime.date.today())+".json"
    print(path)
    order_file1 = open(path, "r")
    print("!")
    order_obj = order_file1.read()
    order_json = json.loads(order_obj)
    
    if int(order_json[str(item)]) > 1:
        order_json[str(item)] = str(int(order_json[str(item)]) - 1)
    else:
        order_json.pop(str(item))
    order_file = open(r".\orders\\"+str(username)+str(datetime.date.today())+".json", "w")
    order_json = json.dumps(order_json)
    order_file.write(order_json)
    order_file.close()

def delete_items(item, username):
    path = ".\orders\\"+str(username)+str(datetime.date.today())+".json"
    print(path)
    order_file1 = open(path, "r")
    print("!")
    order_obj = order_file1.read()
    order_json = json.loads(order_obj)

    order_json.pop(str(item))
    order_file = open(r".\orders\\"+str(username)+str(datetime.date.today())+".json", "w")
    order_json = json.dumps(order_json)
    order_file.write(order_json)
    order_file.close()

def delete_all(username):
    path = ".\orders\\"+str(username)+str(datetime.date.today())+".json"
    print(path)
    order_file1 = open(path, "w")
    order_file1.write("{}")
    order_file1.close()
    