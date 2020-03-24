from flask import Flask, redirect, render_template, request
import db_for_home, db_search

app = Flask(__name__)

# -----------------------------------------------------------#

@app.route("/")
def get_home():
    return redirect("/login")

# default route, not used here

# -----------------------------------------------------------#

@app.route("/<username>/<page_num>")
def home(username, page_num):
    
    get_40 = db_for_home.show_40(page_num=page_num)

    if get_40 == "exception":
        return redirect("/"+username+"/1")
    
    else:    
        next1 = "/"+str(username)+"/"+str(int(page_num)+1)
        back1 = "/"+str(username)+"/"+str(int(page_num)-1)
        print(next1)
        return render_template("home.html",
         username=username, get_40=get_40, page_num=page_num, next1=next1,
         back1=back1)

# central part, need to add search bar
# need to make the shopping bag and ability to add to it
# jumping to certain page
# ability to choose how much of each object to add
# check out option

# -----------------------------------------------------------#

@app.route("/login", methods=['POST','GET'])
def login():
    try:
        user = str(request.form["user"])
        print(user)
        password = str(request.form["password"])
        print(password)
    
        if user == "ori" and password == "gever":
            return redirect("/"+user+"/"+str(1))
        else:
            return redirect("/login")
            
    except:
        print("nothing")
    return render_template("login.html")

# the login page, requires work, need to add the users to db 
# and retrieve their pass to validate, and not let passing through
# straight to the shopping part

# -----------------------------------------------------------#

@app.route("/<username>/search/")
def search(username):
    
    search_list = db_search.search("פסטה")

    return render_template("search.html", 
    search_list=search_list, username=username)


if __name__ == "__main__":
    app.run(debug=True)