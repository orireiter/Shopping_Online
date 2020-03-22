from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route("/")
def get_home():
    return redirect("/home")


@app.route("/home/<username>")
def home(username):
    return render_template("home.html", username=username)

@app.route("/login", methods=['POST','GET'])
def login():
    try:
        user = str(request.form["user"])
        print(user)
        password = str(request.form["password"])
        print(password)
    
        if user == "ori" and password == "gever":
            return redirect("/home/"+user)
        else:
            return redirect("/login")
            
    except:
        print("nothing")
    return render_template("login.html")



if __name__ == "__main__":
    app.run(debug=True)