from flask import *
import hashlib
import sqlite3  

app = Flask(__name__)  

@app.route('/',methods=['GET']) 
def authenticate_user(): 
    # open database
    dbConnectTokens = sqlite3.connect('tokens')
    dbTOKENS = dbConnectTokens.execute("select * from CookieTokens")

    # compare the cookie token with tokens in database
    read_cookie_token = str(request.cookies.get("token"))
    print("got this cookie: token=",read_cookie_token)
    for entry in dbTOKENS:
        if entry[0] == read_cookie_token:
            print ("well you are already registered. Redirect to home page")
            dbConnectTokens.close()
            return redirect("/home_page")

    dbConnectTokens.close()
    res = make_response(render_template("login.html"))
    return res

@app.route('/register_user',methods=['GET','POST'])
def register_user():
    # make a new entry into accounts database
    if request.method == 'POST':
        userName = request.form.get('username')
        passWord = request.form.get('password')
        print("Signing up :::: username:",userName,"    password:",passWord)

        dbConnectAccounts = sqlite3.connect('accounts')
        dbACCOUNTS = dbConnectAccounts.execute("select * from Accounts")
        
        # check if user already exists
        for entry in dbACCOUNTS:
            if entry[0] == str(userName):
                return "you are already registered, Please login"

        dbConnectAccounts.execute("INSERT INTO Accounts(USER, PASSWORD) VALUES(?,?)", (str(userName),str(passWord)));
        dbConnectAccounts.commit()
        dbConnectAccounts.close()

        return redirect("/")

    res = make_response(render_template('signup.html'))
    return res  

@app.route('/home_page',methods=['GET', 'POST'])
def home_page():

    dbConnectTokens = sqlite3.connect('tokens')
    dbTOKENS = dbConnectTokens.execute("select * from CookieTokens")

    read_cookie_token = str(request.cookies.get("token"))
    print("got this cookie: token=",read_cookie_token)
    for entry in dbTOKENS:
        if read_cookie_token == entry[0]:
            logout = str(request.form.get("logout"))
            print("logging out = ", logout)

            if logout=="True":
                res = make_response(render_template("login.html"))
                res.set_cookie('token',"00")    # reset the cookie
                
                # delete from database
                dbConnectTokens.execute("DELETE FROM CookieTokens WHERE ID=(?)",(read_cookie_token,))
                dbConnectTokens.commit()
                dbConnectTokens.close()

                return res

            dbConnectTokens.close()
            res = make_response(render_template("home_page.html",username=entry[1]))
            return res

    dbConnectTokens.close()        
    return "well you are unregistered user. Go home fella.. go home"

@app.route('/verify_user',methods=['POST'])
def verify_user():

    userName = request.form.get('username')
    passWord = request.form.get('password')
    print("userName:",userName,"    password:",passWord)  

    token = hashlib.md5((str(userName) + str(passWord)).encode('utf-8'))
    print("token generated :",token.hexdigest())

    # search in database if user exists
    # if yes -> assign token and save token to cookies and database  
    dbConnectAccounts = sqlite3.connect('accounts')
    dbACCOUNTS = dbConnectAccounts.execute("select * from Accounts")

    dbConnectTokens = sqlite3.connect('tokens')
    dbTOKENS = dbConnectTokens.execute("select * from CookieTokens")

    for entry in dbACCOUNTS:
        if str(userName) == entry[0] and str(passWord)==entry[1]:
            print("creating token for : ", str(userName))
            dbConnectTokens.execute("INSERT INTO CookieTokens(ID, USER) VALUES(?,?)", (str(token.hexdigest()),str(userName)))
            dbConnectTokens.commit()
            dbConnectTokens.close()
            dbConnectAccounts.close()
            print ("well you are already registered. Redirect to home page")
            res = make_response(render_template("home_page.html",username=userName))
            res.set_cookie('token',token.hexdigest())
            return res
    
    print ("well you are unregistered user.")
    res = make_response(render_template("login.html"))
    dbConnectAccounts.close()
    return res
  
if __name__ == '__main__':  
    app.run(debug = True)  