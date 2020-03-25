from flask import Flask, redirect, render_template, request
import db_for_home, db_search, shopping_processor

app = Flask(__name__)


@app.route("/shop/<username>")
def shopping_bag(username):
    amount, item_names = shopping_processor.load_order(username=username)
    length_of_list = range(len(amount))
    
    return render_template("shopping_bag.html",
    username=username, amount=amount, item_names=item_names, leng=length_of_list)




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

@app.route("/delete_all", methods=['POST'])
def delete_all():
    try:
        user3 = request.form['delete_all']
        
        shopping_processor.delete_all(username=user3)
    except:
        print("cant delete")
    back1 = request.referrer
    return redirect(back1) 
app.run(debug=True, port=5001)