from flask import Flask, redirect, render_template, request
import db_for_home, db_search, db_for_auth, db_url_check

app = Flask(__name__)

# -----------------------------------------------------------#

@app.route("/")
def get_home():
    return redirect("/login")

# default route, not used here

# -----------------------------------------------------------#

@app.route("/<id>/<username>/<page_num>")
def home(username, page_num, id):
    
    authenticate = db_url_check.url_check(username=username, id=id)

    if authenticate != True :
        return redirect("/login")
    try:
        get_40 = db_for_home.show_40(page_num=page_num)
    except:
        return redirect("/"+str(id)+"/"+username+"/1")
    if get_40 == "exception":
        return redirect("/"+str(id)+"/"+username+"/1")
    
    else:    
        next1 = "/"+str(id)+"/"+str(username)+"/"+str(int(page_num)+1)
        back1 = "/"+str(id)+"/"+str(username)+"/"+str(int(page_num)-1)
        print(next1)
        yot = r"..\\..\\static\\yotvata_logo.png"
        return render_template("home.html",
         username=username, get_40=get_40, page_num=page_num, next1=next1,
         back1=back1, id=id, yot=yot)

# central part
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
    
        answer, id  = db_for_auth.login(username=user, password=password)
    except:
        print("no answer fromm db")
        return render_template("login.html")
    
    if answer == False:
        print("wrong user or pass")
        return render_template("login.html")
    else:
        print('login good')
        home = "/"+str(id)+"/"+str(user)+"/1"
        return redirect(home)

# the login page, requires work, need to add the users to db 
# and retrieve their pass to validate, and not let passing through
# straight to the shopping part


# -----------------------------------------------------------#
# regisration stuff
@app.route("/register", methods=['GET'])
def register():
    
    return render_template("register.html")


@app.route("/register_process", methods=['POST'])
def register_proccess():
    try:
        backos = request.referrer
        user = str(request.form["user"])
        print(user)
        password = str(request.form["password"])
        print(password)
        tel = str(request.form["tel"])
        print(tel)
        email = str(request.form["email"])
        print(email)
            
    except:
        print("nothing")
        return "error with registration", 404 
    
    if user == "" or password =="" or email == "" or tel == "":
        return redirect(backos)
    
    if len(user) == user.count(" ") or len(password) == password.count(" ") or len(email) == " " or len(tel) == tel.count(" "):
        return redirect(backos)
    
    registered = db_for_auth.register(username=user,password=password,email=email,tel=tel)
    if registered == False:
        return redirect(backos)
    return redirect("/login")

# -----------------------------------------------------------#
# search stuff
@app.route("/search/<id>/<username>", methods=['POST','GET'])
def search(username, id):
    
    authenticate = db_url_check.url_check(username=username, id=id)

    if authenticate != True :
        return redirect("/login")
    
    try:
        query = str(request.form["query"])
        search_list = db_search.search(query)
        
        if search_list == "klum":
            return redirect(request.referrer)
        back2 = request.referrer
        yot = r"..\\..\\static\\yotvata_logo.png"
        return render_template("search.html", 
        search_list=search_list, username=username,yot=yot, back2=back2, query=query, id=id)
    except:
        return redirect("/"+str(id)+"/"+str(username)+"/"+"1")

# ----------------------------------------------------------#

if __name__ == "__main__":
    app.run(debug=False, host='172.16.0.17')