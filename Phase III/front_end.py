from API import *
from database import *
from flask import Flask, render_template, json, request, Response
from decimal import Decimal

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
            return render_template('home.html')
        else:
            return render_template("login.html", error="Credentials Incorrect")

@app.route("/to_register")
def to_register():
    """
    Takes user to register page
    """
    print "toregister start"
    return render_template('register.html', error="")

@app.route("/register", methods=["POST"])
def register():
    """
    Registers user then takes them to the home page
    """
    print "register start"
    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        p1 = request.form['p1']
        p2 = request.form['p2']
        buzzcard = request.form['withCard']
        print p1
        print p2

        error = "Passwords do not match"
        if p1 != p2:
            return render_template("register.html", error = error)
        else:
            if buzzcard == "withoutCard":
                num = generate_bc()
            else:
                print "choose with card"
                num = request.form['BreezeCardNum']
                print num
            add_breezecard(num, name)
            result = check_register(name, p1, email)
            if result == 1:
                global logged_user
                logged_user = name
                return render_template("home.html")
            else:
                error = "Unknown error occurred"
            return render_template("register.html", error=error)

@app.route("/to_station_management")
def to_station_management():
    station_list = get_station_list()
    return render_template('StationListing.html', station_list = station_list, error="")

@app.route("/station_management", methods=["POST"])
def station_management():
    print "station_management start"
    if request.method == "POST":

        station_id_selected = request.form['row_select']
        print station_id_selected
        station_info_tuple = get_station_info(station_id_selected)
        print station_info_tuple
        return render_template('StationDetail.html', station_info_tuple = station_info_tuple)

@app.route("/to_create_new_station")
def to_create_new_station():
    return render_template('CreateNewStation.html', error = "")

@app.route("/create_new_station", methods=["POST"])
def create_new_station():
    print "create_new_station start"
    if request.method == "POST":
        station_name = request.form['station_name']
        station_id = request.form['station_id']
        station_fare = request.form['station_fare']
        BusOrTrain = request.form['BusOrTrain']
        if BusOrTrain == 'Bus':
            train_status = 0
        else:
            train_status = 1
        station_status = request.form['station_status']
        if station_status == 'Open':
            close_status = 0
        else:
            close_status = 1
        # TODO: create new station into database
        result = insert_station(str(station_id), str(station_name), float(station_fare), int(close_status), int(train_status))
        print str(station_name) + str(station_id) + str(station_fare) + str(close_status) + str(train_status)
        if result == 0:
            station_list = get_station_list()
            return render_template('StationListing.html', station_list = station_list)
        else:
            return render_template('CreateNewStation.html', error = "something goes wrong")

@app.route("/to_admin")
def to_admin():
    return render_template('admin.html')

@app.route("/to_suspend_card")
def to_suspend_card():
    return render_template('admin.html')

@app.route("/to_breeze_card")
def to_breeze_card():
    bc_list = get_bc_list()
    # bc_list = (('0475861680208144', Decimal('35.25'), 'commuter14'), )
    return render_template('BreezeCardManage.html', card_list = bc_list, error = "")

@app.route("/filter_bc", methods=["POST"])
def filter_bc():
    print "filter_bc start"
    if request.method == "POST":
        owner = request.form['owner']
        card_number = request.form['card_number']
        min_value = request.form['min_value']
        max_value = request.form['max_value']
        print owner
        print card_number
        if owner != "":
            print "come to owner"
            bc_list = get_bc_list(None, owner, None, None)
        elif card_number != "":
            print "come to number"
            bc_list = get_bc_list(card_number, None, None)
        else:
            bc_list = get_bc_list()
        print bc_list
        return render_template('BreezeCardManage.html', card_list = bc_list, error = "")

@app.route("/breezecard_action", methods=["POST"])
def breezecard_action():
    print "breezecard_action start"
    error = "successfully changed"
    if request.method == "POST":
        stationId = request.form['row_select']
        if (request.form['isset'] == "transfer_name"):
            username = request.form['transfer_name']
            result = bc_change_user(stationId, username)
            if result == 1:
                error = "Whoops, something goes wrong"
        elif (request.form['isset'] == 'set_value'):
            set_value = request.form['set_value']
            result = bc_change_value(stationId, float(set_value))
            if result == 1:
                error = "Whoops, something goes wrong"
        else:
            error = "some error about clicking"
    bc_list = get_bc_list()
    return render_template('BreezeCardManage.html', card_list = bc_list, error = error)






if __name__ == '__main__':
    app.run()
