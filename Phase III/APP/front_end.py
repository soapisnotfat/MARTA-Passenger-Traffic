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
    set_connection()
    return render_template('login.html', error = "")

@app.route("/to_login")
def to_login():
    """
    Takes user to login page
    """
    global logged_user
    logged_user = ""
    return render_template("login.html", error = "")

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
            return render_template('admin.html', error = "")
        elif num == 2:
            global logged_user
            logged_user = _name
            bc_list = get_bc_list("", logged_user, "", "")
            selected_card = bc_list[0]
            bc_back_list = list(bc_list)
            bc_back_list.remove(selected_card)
            bc_list = tuple(bc_back_list)
            bc_back_list = []
            unsuspended_list = bc_unsuspended_list()
            for e in bc_list:
                if e not in unsuspended_list:
                    new_e = list(e)
                    new_e.append("suspended")
                    e = tuple(new_e)
                else:
                    new_e = list(e)
                    new_e.append("")
                    e = tuple(new_e)
                bc_back_list.append(e)
            bc_list = tuple(bc_back_list)
            wheter_intrip = inTrip(_name)
            station_list = get_station_list(0)
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
            return render_template('home.html', startList = startList, card_list = bc_list, in_trip = in_trip, endList = endList, error = "", selected_card = selected_card)
        else:
            return render_template("login.html", error="Cannot login, try again")

@app.route("/to_register")
def to_register():
    """
    Takes user to register page
    """
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
        if constraint_email_format(email) == 0:
            return render_template("register.html", error = "Email does not meet with format.")
        if constraint_username_format(name) == 0:
            return render_template("register.html", error = "Username does not meet with format.")

        error = ""
        if p1 != p2:
            return render_template("register.html", error = "Passwords do not match")
        elif constraint_password_format(p1) == 0:
            return render_template("register.html", error = "Passwords does not meet with format")
        else:
            result = check_register(name, p1, email)
            if result == 1:
                if buzzcard == "withoutCard":
                    num = generate_bc()
                else:
                    num = request.form['BreezeCardNum']
                result2 = add_breezecard(num, name)
                if (result2 != 0):
                    error = "Cannot add breezecard"
                    return render_template("register.html", error=error)
                global logged_user
                logged_user = name
                wheter_intrip = inTrip(name)
                station_list = get_station_list(0)
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
                bc_list = get_bc_list("", logged_user, "", "")
                selected_card = bc_list[0]
                bc_back_list = list(bc_list)
                bc_back_list.remove(selected_card)
                bc_list = tuple(bc_back_list)
                bc_back_list = []
                unsuspended_list = bc_unsuspended_list()
                for e in bc_list:
                    if e not in unsuspended_list:
                        new_e = list(e)
                        new_e.append("suspended")
                        e = tuple(new_e)
                    else:
                        new_e = list(e)
                        new_e.append("")
                        e = tuple(new_e)
                    bc_back_list.append(e)
                bc_list = tuple(bc_back_list)
                return render_template('home.html', startList = startList, card_list = bc_list, in_trip = in_trip, endList = endList, error = "", selected_card = selected_card)
            else:
                error = "Cannot register, try again"
                return render_template("register.html", error=error)

@app.route("/to_station_management")
def to_station_management():
    print "to_station_management starts"
    station_list = get_station_list()
    return render_template('StationListing.html', station_list = station_list, error="")

@app.route("/station_management", methods=["POST"])
def station_management():
    print "station_management start"
    if request.method == "POST":
        button_chosen = request.form['station_management']
        station_list = get_station_list()
        station_back_list = list(station_list)
        if button_chosen == "station_name_up":
            station_back_list = sorted(station_back_list, key = lambda x:x[1])
            station_list = tuple(station_back_list)
            return render_template('StationListing.html', station_list = station_list, error="")
        elif button_chosen == "stop_id_up":
            station_back_list = sorted(station_back_list, key = lambda x:x[0])
            station_list = tuple(station_back_list)
            return render_template('StationListing.html', station_list = station_list, error="")
        elif button_chosen == "stop_id_down":
            station_back_list = sorted(station_back_list, key = lambda x: x[0], reverse=True)
            station_list = tuple(station_back_list)
            return render_template('StationListing.html', station_list = station_list, error="")
        elif button_chosen == "fare_up":
            station_back_list = sorted(station_back_list, key = lambda x: x[2])
            station_list = tuple(station_back_list)
            return render_template('StationListing.html', station_list = station_list, error="")
        elif button_chosen == "fare_down":
            station_back_list = sorted(station_back_list, key = lambda x: x[2], reverse=True)
            station_list = tuple(station_back_list)
            return render_template('StationListing.html', station_list = station_list, error="")
        elif button_chosen == "status_up":
            station_back_list = sorted(station_back_list, key = lambda x: x[3])
            station_list = tuple(station_back_list)
            return render_template('StationListing.html', station_list = station_list, error="")
        elif button_chosen == "status_down":
            station_back_list = sorted(station_back_list, key = lambda x: x[3], reverse = True)
            station_list = tuple(station_back_list)
            return render_template('StationListing.html', station_list = station_list, error="")
        station_id_selected = request.form['row_select']
        station_info_tuple = get_station_info(station_id_selected)
        intersection_name = station_info_tuple[-1]
        not_have_intersection = (intersection_name is None)
        return render_template('StationDetail.html', station_info_tuple = station_info_tuple, not_have_intersection = not_have_intersection, intersection_name = intersection_name, error = "")

@app.route("/to_create_new_station")
def to_create_new_station():
    print "to_create_new_station starts"
    return render_template('CreateNewStation.html', error = "")

@app.route("/create_new_station", methods=["POST"])
def create_new_station():
    print "create_new_station start"
    if request.method == "POST":
        station_name = request.form['station_name']
        station_id = request.form['station_id']
        station_fare = request.form['station_fare']
        BusOrTrain = request.form['BusOrTrain']
        station_status = request.form['station_status']
        if station_status == 'Open':
            close_status = 0
        else:
            close_status = 1
        result = -1
        if BusOrTrain == 'Bus':
            train_status = 0
            bus_intersection = request.form['bus_intersection']
            result = insert_station(station_id, station_name, float(station_fare), int(close_status), int(train_status), bus_intersection)
        else:
            train_status = 1
            result = insert_station(station_id, station_name, float(station_fare), int(close_status), int(train_status))
        if result == 0:
            station_list = get_station_list()
            return render_template('StationListing.html', station_list = station_list, error = "")
        elif result == 1000:
            return render_template('CreateNewStation.html', error = "station fare is not valid")
        else:
            return render_template('CreateNewStation.html', error = "something goes wrong")


@app.route("/update_station_detail", methods=["POST"])
def update_station_detail():
    print "update_station_detail start"
    if request.method == "POST":
        button_chosen = request.form['update_station_detail']
        if button_chosen == 'update_fare':
            new_fare = request.form['fare']
            stop_id = request.form['station_id']
            result = station_update_fare(stop_id, float(new_fare))
            error = ""
            if result == 1000:
                error = "cannot update fare because it is not between [0, 50.0]"
            else:
                error = "whoops, something wrong with updating fare"
            station_list = get_station_list()
            return render_template('StationListing.html', station_list = station_list, error = error)
        else:
            new_status = request.form['status_selected']
            stop_id = request.form['station_id']
            result = station_update_closedstatus(stop_id, int(new_status))
            error = ""
            if result != 0:
                error = "cannot update status"
            station_list = get_station_list()
            return render_template('StationListing.html', station_list = station_list, error = error)




@app.route("/to_admin")
def to_admin():
    print "to admin starts"
    return render_template('admin.html', error = "")

@app.route("/to_suspend_card")
def to_suspend_card():
    print "to suspend_card starts"
    suspend_card_list = conflict_list()
    return render_template('suspended.html', card_list = suspend_card_list, error = "")

@app.route("/to_breeze_card")
def to_breeze_card():
    print "to_breeze_card"
    bc_list = get_bc_list("", "", "", "")
    bc_back_list = []
    unsuspended_list = bc_unsuspended_list()
    for e in bc_list:
        if e not in unsuspended_list:
            new_e = list(e)
            new_e[-1] = "Suspended"
            e = tuple(new_e)
        bc_back_list.append(e)
    bc_list = tuple(bc_back_list)
    # bc_list = (('0475861680208144', Decimal('35.25'), 'commuter14'), )
    return render_template('BreezeCardManage.html', card_list = bc_list, error = "", show_suspended = True)

@app.route("/filter_bc_and_isset", methods=["POST"])
def filter_bc_and_isset():
    if request.method == "POST":
        print "filter_bc_and_isset"
        button_chosen = request.form['filter_bc_and_isset']
        if button_chosen == "update_filter":
            owner = request.form['owner']
            card_number = request.form['card_number']
            min_value = request.form['min_value']
            max_value = request.form['max_value']
            whether_suspended = request.form['suspended_status']
            bc_list = get_bc_list(card_number, owner, min_value, max_value)
            bc_back_list = []
            unsuspended_list = bc_unsuspended_list()
            # not show suspended_list
            if whether_suspended == '0':
                show_suspended_status = False
                for e in bc_list:
                    if e in unsuspended_list:
                        bc_back_list.append(e)
            else:
                show_suspended_status = True
                for e in bc_list:
                    if e not in unsuspended_list:
                        new_e = list(e)
                        new_e[-1] = "Suspended"
                        e = tuple(new_e)
                    bc_back_list.append(e)
            bc_list = tuple(bc_back_list)
            return render_template('BreezeCardManage.html', card_list = bc_list, error = "", show_suspended = show_suspended_status)

        elif button_chosen == "set_value" or button_chosen == "transfer_name":
            error = ""
            stationId = request.form['row_select']
            if (button_chosen == "transfer_name"):
                username = request.form['transfer_name']
                if username == "":
                    error = "Whoops, need to input new_user"
                elif isAdmin(username) == 1:
                    error = "cannot transfer to admin"
                else:
                    original_username = bc_info(stationId)
                    original_username = original_username[0]
                    original_username = original_username[2]
                    whether_in_trip = inTrip(original_username)
                    if whether_in_trip[0] and whether_in_trip[1][2] == stationId:
                        error = "You cannot transfer a card which is in_trip."
                    else:
                        result = bc_change_user(stationId, username)
                        if result != 0:
                            error = "Whoops, cannot transfer to this person."
            elif (button_chosen == 'set_value'):
                set_value = request.form['set_value']
                result = bc_change_value(stationId, float(set_value))
                if result != 0:
                    error = "Whoops, something goes wrong"
            else:
                error = "some error about clicking"
            bc_list = get_bc_list("", "", "", "")
            bc_back_list = []
            unsuspended_list = bc_unsuspended_list()
            whether_suspended = request.form['suspended_status']
            if whether_suspended == '0':
                show_suspended_status = False
                for e in bc_list:
                    if e in unsuspended_list:
                        bc_back_list.append(e)
            else:
                show_suspended_status = True
                for e in bc_list:
                    if e not in unsuspended_list:
                        new_e = list(e)
                        new_e[-1] = "Suspended"
                        e = tuple(new_e)
                    bc_back_list.append(e)
            bc_list = tuple(bc_back_list)
            return render_template('BreezeCardManage.html', card_list = bc_list, error = error, show_suspended = show_suspended_status)

@app.route("/to_passenger_flow_report")
def to_passenger_flow_report():
    print "to_passenger_flow_report"
    passenger_list = passenger_flow()
    return render_template('PassengerFlowReport.html', passenger_list = passenger_list, error = "")

@app.route("/update_passenger_flow", methods=["POST"])
def update_passenger_flow():
    print "update_passenger_flow start"
    error = ""
    if request.method == "POST":
        button_chosen = request.form['update_passenger_flow']
        if button_chosen == 'station_name_up':
            passenger_list = passenger_flow()
            passenger_back_list = list(passenger_list)
            passenger_back_list = sorted(passenger_back_list, key = lambda x:x[0])
            passenger_list = tuple(passenger_back_list)
        else:
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            if start_time == "" and end_time == "":
                passenger_list = passenger_flow()
            elif start_time == "":
                passenger_list = passenger_flow(None, end_time)
            elif end_time == "":
                passenger_list = passenger_flow(start_time, None)
            else:
                passenger_list = passenger_flow(start_time, end_time)
            # passenger_list = passenger_flow(start_time, end_time)
        return render_template('PassengerFlowReport.html', passenger_list = passenger_list, error = "")


@app.route("/balance_or_start", methods=["POST"])
def balance_or_start():
    print "balance_or_start start"
    if request.method == "POST":
        selected_card_num = request.form['card_selected']
        button_chosen = request.form['balance_or_start']
        error = ""
        if button_chosen == 'start_trip':
            start_station = request.form['start_selected']
            result = take_trip(selected_card_num, start_station)
            error = ""
            if result != 0:
                error = "cannot take the trip"
        elif button_chosen == "user_end_trip":
            end_station = request.form['end_selected']
            result = end_trip(logged_user, end_station)
            error = ""
            if result == 1:
                error = "some error happens when ending the trip"
            elif result == 2:
                error = "You must end at the same stop type as ur start station"
            elif result == 3:
                error = "You are not in a trip"
        selected_card = bc_info(selected_card_num)
        selected_card = selected_card[0]
        bc_list = get_bc_list("", logged_user, "", "")
        bc_back_list = list(bc_list)
        bc_back_list.remove(selected_card)
        bc_list = tuple(bc_back_list)
        bc_back_list = []
        unsuspended_list = bc_unsuspended_list()
        for e in bc_list:
            if e not in unsuspended_list:
                new_e = list(e)
                new_e.append("suspended")
                e = tuple(new_e)
            else:
                new_e = list(e)
                new_e.append("")
                e = tuple(new_e)
            bc_back_list.append(e)
        bc_list = tuple(bc_back_list)

        wheter_intrip = inTrip(logged_user)
        station_list = get_station_list(0)
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
        return render_template('home.html', startList = startList, card_list = bc_back_list, in_trip = in_trip, endList = endList, error = error, selected_card = selected_card)

@app.route("/to_maganage_card")
def to_maganage_card():
    print "to_maganage_card"
    card_list = bc_unsuspended_list(logged_user)
    return render_template('manageCard.html', card_list = card_list, error="")

@app.route("/manage_card_function", methods=["POST"])
def manage_card_function():
    print "manage_card_function start"
    error = ""
    if request.method == "POST":
        button_chosen = request.form['manage_card_function']
        if button_chosen == "remove":
            card_list = get_bc_list("", logged_user, "", "")
            card_len = len(card_list)
            if card_len == 1:
                error = "cannot remove card"
            else:
                card_selected_num = request.form['card_selected']
                result = remove_breezecard(card_selected_num)
                if result != 0:
                    error = "cannot remove card"
        elif button_chosen == "add_card":
            card_selected_num = request.form['add_card']
            result = add_breezecard(card_selected_num, logged_user)
            if result != 0:
                error = "cannot add card to user"
            else:
                error = ""

        elif button_chosen == "add_value":
            card_selected_num = request.form['card_selected']
            add_money = float(request.form['money_value'])
            result = bc_add_value(card_selected_num, add_money)
            if result == 1000:
                error = "Invalid add money amount"
            elif result != 0:
                error = "cannot add money to this card"
        card_list = bc_unsuspended_list(logged_user)
        card_back_list = list(card_list)
        if button_chosen == "card_number_up":
            card_back_list = sorted(card_back_list, key = lambda x:x[0])
        elif button_chosen == "card_number_down":
            card_back_list = sorted(card_back_list, key = lambda x:x[0], reverse = True)
        elif button_chosen == "value_up":
            card_back_list = sorted(card_back_list, key = lambda x:x[1])
        elif button_chosen == "value_down":
            card_back_list = sorted(card_back_list, key = lambda x:x[1], reverse = True)
        card_list = tuple(card_back_list)
        return render_template('manageCard.html', card_list = card_list, error=error)

@app.route("/to_home")
def to_home():
    print "to_home function"
    card_list = bc_unsuspended_list(logged_user)

    selected_card = card_list[0]

    bc_list = get_bc_list("", logged_user, "", "")
    bc_back_list = list(bc_list)
    bc_back_list.remove(selected_card)
    bc_list = tuple(bc_back_list)
    bc_back_list = []
    unsuspended_list = bc_unsuspended_list()
    for e in bc_list:
        if e not in unsuspended_list:
            new_e = list(e)
            new_e.append("suspended")
            e = tuple(new_e)
        else:
            new_e = list(e)
            new_e.append("")
            e = tuple(new_e)
        bc_back_list.append(e)
    bc_list = tuple(bc_back_list)
    wheter_intrip = inTrip(logged_user)
    station_list = get_station_list(0)
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
    return render_template('home.html', startList = startList, card_list = bc_list, in_trip = in_trip, endList = endList, error = "", selected_card = selected_card)

@app.route("/to_view_trip_history")
def to_view_trip_history():
    print "to_view_trip_history"
    trip_list = trip_history(logged_user)
    return render_template('TripHistory.html', trip_list = trip_list, error="")

@app.route("/update_view_history", methods=["POST"])
def update_view_history():
    print "update_view_history start"
    if request.method == "POST":
        button_chosen = request.form['update_view_history']
        if button_chosen == 'update_filter':
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            if start_time == "" and end_time == "":
                trip_list = trip_history(logged_user)
            elif start_time == "":
                trip_list = trip_history(logged_user, None, end_time)
            elif end_time == "":
                trip_list = trip_history(logged_user, start_time, None)
            else:
                trip_list = trip_history(logged_user, start_time, end_time)
            return render_template('TripHistory.html', trip_list = trip_list, error="")
        else:
            trip_list = trip_history(logged_user)
            trip_back_list = list(trip_list)
            trip_back_list = sorted(trip_back_list, key = lambda x: x[0], reverse=True)
            trip_list = tuple(trip_back_list)
            return render_template('TripHistory.html', trip_list = trip_list, error="")

@app.route("/suspended_reassign", methods=["POST"])
def suspended_reassign():
    print "suspended_reassign start"
    error = ""
    if request.method == "POST":
        button_chosen = request.form['suspended_reassign']
        if button_chosen == "set_new_owner" or button_chosen == "set_old_owner":
            suspended_card_num =request.form['card_selected']
            suspend_card_list = conflict_list()
            suspended_card_selected = ()
            for i in suspend_card_list:
                if i[0] == suspended_card_num:
                    suspended_card_selected = i
            if button_chosen == "set_new_owner":
                new_owner = suspended_card_selected[1]
            else:
                new_owner = suspended_card_selected[3]
            result = bc_change_user(suspended_card_num, new_owner)
            if result != 0:
                error = "did not change successfully"
            else:
                result2 = bc_remove_from_conflict(suspended_card_selected[1], suspended_card_selected[0])
                if result2 != 0:
                    error = "did not remove from conflict_list successfully"
            suspend_card_list = conflict_list()
            return render_template('suspended.html', card_list = suspend_card_list, error = error)
        else:
            suspend_card_list = conflict_list()
            suspend_back_list = list(suspend_card_list)
            if button_chosen == "date_suspended_down":
                suspend_back_list = sorted(suspend_back_list, key = lambda x:x[2], reverse = True)
            elif button_chosen == "date_suspended_up":
                suspend_back_list = sorted(suspend_back_list, key = lambda x:x[2])
            else:
                suspend_back_list = sorted(suspend_back_list, key = lambda x:x[0])
            suspend_card_list = tuple(suspend_back_list)
            return render_template('suspended.html', card_list = suspend_card_list, error = "")


if __name__ == '__main__':
    app.run()
