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
            card_list = get_bc_list(None, _name, None, None)

            selected_card = card_list[0]

            card_list_list = list(card_list)
            card_list_list.remove(selected_card)
            card_list = tuple(card_list_list)
            wheter_intrip = inTrip(_name)
            station_list = get_station_list()
            if wheter_intrip[0]:
                in_trip = True
                stopNAME = (get_station_info(wheter_intrip[1][3]))[1]
                startList = (((stopNAME,wheter_intrip[1][0]), wheter_intrip[1][3]),)
            else:
                in_trip = False
                startList = []
                for i in station_list:
                    startList.append(((i[1], i[2]), i[0]))
                startList = tuple(startList)
            endList = []
            for i in station_list:
                endList.append((i[1], i[0]),)
            startList = tuple(startList)
            print selected_card
            return render_template('home.html', startList = startList, card_list = card_list, in_trip = in_trip, endList = endList, error = "", selected_card = selected_card)
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
                card_list = get_bc_list(None, name, None, None)
                wheter_intrip = inTrip(name)
                station_list = get_station_list()
                if wheter_intrip[0]:
                    in_trip = True
                    stopNAME = (get_station_info(wheter_intrip[1][3]))[1]
                    startList = (((stopNAME,wheter_intrip[1][0]), wheter_intrip[1][3]),)
                else:
                    in_trip = False
                    startList = []
                    for i in station_list:
                        startList.append(((i[1], i[2]), i[0]))
                    startList = tuple(startList)
                endList = []
                for i in station_list:
                    endList.append((i[1], i[0]),)
                startList = tuple(startList)
                return render_template('home.html', startList = startList, card_list = card_list, in_trip = in_trip, endList = endList, error = "")
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
    suspend_card_list = conflict_list()
    return render_template('suspended.html', card_list = suspend_card_list, error = "")

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

@app.route("/to_passenger_flow_report")
def to_passenger_flow_report():
    passenger_list = passenger_flow()
    return render_template('PassengerFlowReport.html', passenger_list = passenger_list, error = "")

@app.route("/update_passenger_flow", methods=["POST"])
def update_passenger_flow():
    print "update_passenger_flow start"
    error = "successfully changed"
    if request.method == "POST":
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        passenger_list = passenger_flow(start_time, end_time)
        return render_template('PassengerFlowReport.html', passenger_list = passenger_list, error = "")


@app.route("/balance_or_start", methods=["POST"])
def balance_or_start():
    print "balance_or_start start"
    if request.method == "POST":
        selected_card_num = request.form['card_selected']
        button_chosen = request.form['balance_or_start']
        error = ""
        if button_chosen == 'start_trip':
            print "get into start_trip"
            start_station = request.form['start_selected']
            print start_station
            result = take_trip(selected_card_num, start_station)
            error = ""
            if result != 0:
                error = "cannot take the trip"
            else:
                error = "successfully take trip"
            print error
        elif button_chosen == "user_end_trip":
            end_station = request.form['end_selected']
            print end_station
            result = end_trip(logged_user, end_station)
            error = ""
            if result != 0:
                error = "cannot end the trip"
        selected_card = bc_info(selected_card_num)
        selected_card = selected_card[0]
        print selected_card
        card_list = get_bc_list(None, logged_user, None, None)
        card_list_list = list(card_list)
        card_list_list.remove(selected_card)
        card_list = tuple(card_list_list)
        wheter_intrip = inTrip(logged_user)
        station_list = get_station_list()
        if wheter_intrip[0]:
            in_trip = True
            stopNAME = (get_station_info(wheter_intrip[1][3]))[1]
            startList = (((stopNAME,wheter_intrip[1][0]), wheter_intrip[1][3]),)
        else:
            in_trip = False
            startList = []
            for i in station_list:
                startList.append(((i[1], i[2]), i[0]))
            startList = tuple(startList)
        endList = []
        for i in station_list:
            endList.append((i[1], i[0]),)
        startList = tuple(startList)
        return render_template('home.html', startList = startList, card_list = card_list, in_trip = in_trip, endList = endList, error = "", selected_card = selected_card)

@app.route("/to_maganage_card")
def to_maganage_card():
    card_list = get_bc_list(None, logged_user, None, None)
    return render_template('manageCard.html', card_list = card_list, error="")

@app.route("/manage_card_function", methods=["POST"])
def manage_card_function():
    print "manage_card_function start"
    error = ""
    if request.method == "POST":
        button_chosen = request.form['manage_card_function']
        if button_chosen == "remove":
            card_selected_num = request.form['card_selected']
            result = bc_change_user(card_selected_num, None)
            if result != 0:
                error = "cannot remove card"
        elif button_chosen == "add_card":
            card_selected_num = request.form['add_card']
            result = add_breezecard(card_selected_num, logged_user)
            if result != 0:
                error = "cannot add card to user"
            else:
                error = "add card successfully"

        elif button_chosen == "add_value":
            card_selected_num = request.form['card_selected']
            add_money = float(request.form['money_value'])
            result = bc_add_value(card_selected_num, add_money)
            if result != 0:
                error = "cannot add money to this card"
        card_list = get_bc_list(None, logged_user, None, None)
        return render_template('manageCard.html', card_list = card_list, error=error)

@app.route("/to_home")
def to_home():
    card_list = get_bc_list(None, logged_user, None, None)

    selected_card = card_list[0]

    card_list_list = list(card_list)
    card_list_list.remove(selected_card)
    card_list = tuple(card_list_list)
    wheter_intrip = inTrip(logged_user)
    station_list = get_station_list()
    if wheter_intrip[0]:
        in_trip = True
        stopNAME = (get_station_info(wheter_intrip[1][3]))[1]
        startList = (((stopNAME,wheter_intrip[1][0]), wheter_intrip[1][3]),)
    else:
        in_trip = False
        startList = []
        for i in station_list:
            startList.append(((i[1], i[2]), i[0]))
        startList = tuple(startList)
    endList = []
    for i in station_list:
        endList.append((i[1], i[0]),)
    startList = tuple(startList)
    print selected_card
    return render_template('home.html', startList = startList, card_list = card_list, in_trip = in_trip, endList = endList, error = "", selected_card = selected_card)

@app.route("/to_view_trip_history")
def to_view_trip_history():
    trip_list = trip_history(logged_user)
    return render_template('TripHistory.html', trip_list = trip_list, error="")

@app.route("/update_view_history", methods=["POST"])
def update_view_history():
    print "update_view_history start"
    error = "successfully changed"
    if request.method == "POST":
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        trip_list = trip_history(logged_user)
        return render_template('TripHistory.html', trip_list = trip_list, error=error)

@app.route("/suspended_reassign", methods=["POST"])
def suspended_reassign():
    print "suspended_reassign start"
    error = ""
    if request.method == "POST":
        suspended_card_num =request.form['card_selected']
        button_chosen = request.form['suspended_reassign']
        suspend_card_list = conflict_list()
        suspended_card_selected = ()
        for i in suspend_card_list:
            if i[0] == suspended_card_num:
                suspended_card_selected = i

        if button_chosen == "set_new_owner":
            new_owner = suspended_card_selected[1]
        else:
            new_owner = suspended_card_selected[3]
        print "new_owner is ",
        print new_owner
        result = bc_change_user(suspended_card_num, new_owner)
        if result != 0:
            error = "did not change successfully"
        suspend_card_list = conflict_list()
        return render_template('suspended.html', card_list = suspend_card_list, error = error)


if __name__ == '__main__':
    app.run()
