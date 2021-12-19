from flask import *
import hashlib

from ..db_class import database

DBaccounts = database("./database/accounts",table="Accounts")
DBtokens = database(database="./database/tokens",table="CookieTokens")


def authenticate_user(request): 
    # read database
    tokens = DBtokens.read()

    # compare the cookie token with tokens in database
    read_cookie_token = str(request.cookies.get("token"))
    print("got this cookie: token=",read_cookie_token)
    for entry in tokens:
        if entry[0] == read_cookie_token:
            print ("well you are already registered. Redirect to home page")
            return redirect("/home_page")

    res = make_response(render_template("login.html"))
    return res

def register_user(request):
    # make a new entry into accounts database
    if request.method == 'POST':
        userName = request.form.get('username')
        passWord = request.form.get('password')
        print("Signing up :::: username:",userName,"    password:",passWord)
        
        # check if user already exists
        for entry in accounts:
            if entry[0] == str(userName):
                return "you are already registered, Please login"

        accounts.insert(data=(str(userName),str(passWord)))

        return redirect("/")

    res = make_response(render_template('signup.html'))
    return res 

def home_page(request):
    tokens = DBtokens.read()

    read_cookie_token = str(request.cookies.get("token"))
    print("got this cookie: token=",read_cookie_token)
    for entry in tokens:
        if read_cookie_token == entry[0]:
            logout = str(request.form.get("logout"))
            print("logging out = ", logout)

            if logout=="True":
                # delete from database
                DBtokens.delete(idd=(read_cookie_token,))

                res = make_response(render_template("login.html"))
                res.set_cookie('token',"00")    # reset the cookie
                return res

            res = make_response(render_template('index.html',username=entry[1]))
            return res
       
    return "well you are unregistered user. Go home fella.. go home"

def verify_user(request):
    userName = request.form.get('username')
    passWord = request.form.get('password')
    print("userName:",userName,"    password:",passWord)  

    token = hashlib.md5((str(userName) + str(passWord)).encode('utf-8'))
    print("token generated :",token.hexdigest())

    # search in database if user exists
    # if yes -> assign token and save token to cookies and database
    accounts = DBaccounts.read()
    tokens = DBtokens.read()

    for entry in accounts:
        if str(userName) == entry[0] and str(passWord)==entry[1]:
            print("creating token for : ", str(userName))
            
            # check if token already exist
            for check_token in tokens:
                if check_token[0] == str(token.hexdigest()):
                    print("already logged in somewhere")
                else :
                    DBtokens.insert(data=(str(token.hexdigest()),str(userName)))

            if len(tokens)==0:
                DBtokens.insert(data=(str(token.hexdigest()),str(userName)))

            res = make_response(render_template('index.html',username=userName))
            res.set_cookie('token',token.hexdigest())
            return res
    
    print ("well you are unregistered user.")
    res = make_response(render_template("login.html"))
    return res
