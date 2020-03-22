from flask import Flask, redirect, render_template, request
import db_connect

app = Flask(__name__)


@app.route("/")
def get_home():
    return redirect("/login")


@app.route("/<username>/<page_num>")
def home(username, page_num):
    
    get_40 = db_connect.show_40(page_num=page_num)

    if get_40 == "exception":
        return redirect("/"+username+"/1")
    
    else:    
        return render_template("home.html", username=username, get_40=get_40)

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



if __name__ == "__main__":
    app.run(debug=True)