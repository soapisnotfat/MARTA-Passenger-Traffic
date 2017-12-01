import API
from database import *
from flask import Flask, render_template, json, request, Response

app = Flask(__name__)
#app.debug = True
logged_user = ""
logged_admin = ""

@app.route('/')
def main():
    """
    Starts app at login screen
    """
    # TODO: check whether set up database
    # db.setupConnection()
    set_connection()
    return render_template('login.html')

@app.route("/to_login")
def to_login():
    """
    Takes user to login page
    """
    global logged_user
    logged_user = ""
    return render_template("login.html")

@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    """
    signs in user with given credentials
    Makes call to python wrapper
    logs user in or displays error message
    """

    # read the posted values from the UI
    if request.method == "POST":
        _name = request.form['usr']
        _password = request.form['pwd']
        num = login(_name, _password)

        if num == 1:
            global logged_admin
            logged_admin = _name
            return render_template('admin.html')
        elif num == 2:
            global logged_user
            logged_user = _name
            return render_template('homepage.html')
        else:
            return render_template("login.html", error="Credentials Incorrect")

@app.route("/to_register")
def to_register():
    """
    Takes user to register page
    """
    return render_template('register.html', error="")

@app.route("/register", methods=["POST", "GET"])
def register():
    """
    Registers user then takes them to the home page
    """

    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        p1 = request.form['p1']
        p2 = request.form['p2']
        buzzcard = request.form['withCard']

        error = "Passwords do not match"
        if p1 != p2:
            return render_template("register.html", error=error)
        elif len(p1) < 6:
            error = "Password must be six or more characters"
            return render_template("register.html", error=error)
        else:
            if buzzcard == "withoutCard":
                num = generate_bc()
            else:
                num = request.form['BreezeCardNum']
            add_breezecard(num, name)
            result = register(name, p1, email)
            if result == 1:
                global logged_user
                logged_user = name
                return render_template("homepage.html")
            else:
                error = "Unknown error occurred"
            return render_template("register.html", error=error)

if __name__ == '__main__':
    app.run()
