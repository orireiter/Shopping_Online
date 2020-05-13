from flask import Flask, redirect, render_template, request
import db_for_home, db_search, db_for_auth, db_url_check
import configparser


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

@app.route("/")
def redirecting():
    return redirect("/login")

# default route, not used here

# -----------------------------------------------------------#
# main page, retrieves items from db and their pics,
# includes a shopping bag in an iframe (different port)
# to handle actions more fluently

@app.route("/<id>/<username>/<page_num>")
def home(username, page_num, id):
    
    authenticate = db_url_check.url_check(username=username, id=id)

    if authenticate != True :
        return redirect("/login")
    try:
        ip = get_config("host")
        get_40 = db_for_home.show_40(page_num=page_num)
    except:
        return redirect("/"+str(id)+"/"+username+"/1")
    if get_40 == "exception":
        return redirect("/"+str(id)+"/"+username+"/1")
    
    else:    
        next1 = "/"+str(id)+"/"+str(username)+"/"+str(int(page_num)+1)
        back1 = "/"+str(id)+"/"+str(username)+"/"+str(int(page_num)-1)
        print(next1)
        no_img = r"..\\..\\static\\no_image.png"
        return render_template("home.html",
         username=username, get_40=get_40, page_num=page_num, next1=next1,
         back1=back1, id=id, no_img=no_img, ip=ip)



# -----------------------------------------------------------#
# login page - confirms credentials against db 
# (still unencrypted)

@app.route("/login", methods=['POST','GET'])
def login():
    try:
        user = str(request.form["user"])
        print(user)
        password = str(request.form["password"])
        print(password)
        try:
            user1 = user.replace('"',"''")
        except:
            pass
        answer, id  = db_for_auth.login(username=user1, password=password)
    except:
        print("no answer fromm db")
        return render_template("login.html")
    
    if answer == False:
        print("wrong user or pass")
        return render_template("login.html")
    else:
        print('login good')
        home = "/"+str(id)+"/"+str(user1)+"/1"
        return redirect(home)


# -----------------------------------------------------------#
# regisration stuff
@app.route("/register", methods=['GET'])
def register():
    
    return render_template("register.html")

# when submitting a register form it be sent here,
# handle redirections better
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
# search stuff, same as home, but it shows items according to
# what you searched
@app.route("/search/<id>/<username>", methods=['POST','GET'])
def search(username, id):
    
    authenticate = db_url_check.url_check(username=username, id=id)

    if authenticate != True :
        return redirect("/login")
    
    try:
        ip = get_config("host")
        query = str(request.form["query"])
        search_list = db_search.search(query)
        
        if search_list == "klum":
            return redirect(request.referrer)
        back2 = request.referrer
        no_img = r"..\\..\\static\\no_image.png"
        return render_template("search.html", 
        search_list=search_list, username=username,no_img=no_img, back2=back2, query=query, id=id, ip=ip)
    except:
        return redirect("/"+str(id)+"/"+str(username)+"/"+"1")

# ----------------------------------------------------------#

if __name__ == "__main__":
    host_add = get_config("host")
    
    app.run(debug=True, host=host_add)