import pymongo
from pymongo import MongoClient
# general use imports
import datetime, os, json, email, smtplib, ssl, configparser
# email related
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



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

    collection = get_config("user_col")
    collection = db[collection]
    
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
    
    # email
    # you need to make sure less secure apps can use it!!!
    gmail_user = str(get_config("owner_email"))
    gmail_password = str(get_config("owner_email_pass"))
    print(gmail_user,gmail_password)
    receivers = str(gmail_user)
    subject = f'{datetime.date.today()} registration of: {username}'
    #-------------------#


    #-------------------#
    # formatting a mail #

    raw_mail = MIMEText(f'''name - {username} \n password - {password} \n email -  {email} \n tel -  {tel} ''')
    raw_mail["From"] = gmail_user
    raw_mail["To"] = f'{receivers}'
    raw_mail["Subject"] = f'{subject}'
    
    
    # Add attachment to message and convert message to string
    ready_mail = raw_mail.as_string()
    
    
    try: 
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        mail_server.ehlo()
        mail_server.login(user=gmail_user, password=gmail_password)
        mail_server.sendmail(from_addr=gmail_user, to_addrs=receivers , msg=ready_mail)
        mail_server.close()
        print('mail sent')
    except:
        print("didnt work")

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