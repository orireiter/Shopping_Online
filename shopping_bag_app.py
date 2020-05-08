# flask imports
from flask import Flask, redirect, render_template, request
# homemade imports
import db_for_home, db_search, shopping_processor, barcode_maker
# general use imports
import datetime, os, json, email, smtplib, ssl, configparser
# email related
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



app = Flask(__name__)


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


@app.route("/shop/<username>")
def shopping_bag(username):
    amount, item_names = shopping_processor.load_order(username=username)
    if amount == 'empty':
        amount = ''
        item_names = ''

    length_of_list = range(len(amount))
    ip = get_config("host")
    return render_template("shopping_bag.html",
    username=username, amount=amount, item_names=item_names, leng=length_of_list, ip=ip)




@app.route("/add_item", methods=['POST'])
def add_item():

    try:
        item_user = request.form["add_item"]
        splitted = item_user.split(",")
        print(splitted)
        item = splitted[0]
        username = splitted[1]
        
        shopping_processor.add_item(item=item, username=username)
    except:
        print("didnt work")

    back1 = "/shop/"+str(username)
    return redirect(back1)

@app.route("/add_free_item", methods=['POST'])
def add_free_item():

    try:
        item4 = str(request.form["item"])
        username4 = str(request.form["user"])
        print(item4, username4)
        shopping_processor.add_item(item=item4, username=username4)
    except:
        print("didnt work")

    back1 = "/shop/"+str(username4)
    return redirect(back1)

@app.route("/delete_item", methods=['POST'])
def delete_item():
    try:
        item_user1 = request.form['delete_item']
        splitted = item_user1.split(",")
        
        item1 = splitted[0]
        username1 = splitted[1]
        print(splitted)
        shopping_processor.delete_item(item=item1, username=username1)
    except:
        print("cant delete")
    back1 = request.referrer
    return redirect(back1) 

@app.route("/delete_items", methods=['POST'])
def delete_items():
    try:
        item_user1 = request.form['delete_items']
        splitted = item_user1.split(",")
        
        item2 = splitted[0]
        username2 = splitted[1]
        print(splitted)
        shopping_processor.delete_items(item=item2, username=username2)
    except:
        print("cant delete")
    back1 = request.referrer
    return redirect(back1) 



if __name__ == "__main__":
    host_add = get_config("host")
    
    app.run(debug=True,host=host_add ,port=5001)