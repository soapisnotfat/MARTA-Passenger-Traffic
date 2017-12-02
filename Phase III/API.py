from database import *
from constraint import *
import hashlib
import random


'''
register function that inserts tuples to database

returns
    1 - register successfully
    98 - username doesn't match regex
    99 - password doesn't match regex
    100 - email doesn't match regex
    other - violation caught
'''
def check_register(username, password, email):
    # if constraint_username_format(username) == 0:
    #     # username doesn't match regex
    #     return 98
    # if constraint_password_format(password) == 0:
    #     # password doesn't match regex
    #     return 99
    # if constraint_email_format(email) == 0:
    #     # email doesn't match regex
    #     return 100

    # set up connection
    set_connection()

    # execute the query
    hashed_password = hashlib.md5(password).hexdigest()
    user_insert_result = user_insert(username, hashed_password)
    if user_insert_result == 0:
        passenger_insert_result = passenger_insert(username, email)
        if passenger_insert_result == 0:
            out = 1
        else:
            user_delete(username)
            out = 0
    else:
        out = 0

    # close connection
    close_connection()

    return out

'''
login function

:returns
    0 - login failed
    1 - administrator login
    2 - passenger login
'''
def login(username, password):
    # set up connection
    set_connection()

    # execute the query
    hashed_password = hashlib.md5(password).hexdigest()
    login_response = db_login(username, hashed_password)

    # close connection
    close_connection()

    return login_response

'''
user adds breezecard
- used for register page, in add breezecard section
:returns
    0 - the card doesn't exist
    1 - conflict caught
    2 - successfully add bc to user
    3 - any other violations
'''
def add_breezecard(num, username):
    # set up connection
    set_connection()

    # execute the query
    bc_exist = db_bc_exist(num)
    if bc_exist == 0:
        out = 0
    else:
        bc_info = db_bc_info(num)
        if bc_info[2] is not None:
            # conflict caught
            print("conflict caught")
            # TODO: add conflict to database
            out = 1
        else:
            # update new holder
            update_status = db_bc_update_holder(num, username)
            if update_status == 0:
                out = 2
            else:
                out = 3

    # close connection
    close_connection()

    return out

'''
assign a new user to a breezecard

:returns
    0 - successfully changed username
    1 - any violation
'''
def bc_change_user(num, username):
    # set up connection
    set_connection()

    # execute the query
    update_status = db_bc_update_holder(num, username)

    # close connection
    close_connection()

    return update_status

'''
change a breezecard's value

:returns
    0 - successfully changed value
    1 - any violation
'''
def bc_change_value(num, value):
    # set up connection
    set_connection()

    # execute the query
    update_status = db_bc_update_value(num, value)

    # close connection
    close_connection()

    return update_status


'''
add a certain value to a breezecard

:returns
    0 - successfully added value
    1 - any violation
'''
def bc_add_value(num, value):
    # set up connection
    set_connection()

    # execute the query
    current_card = db_bc_info(num)
    if current_card is None:
        return 1
    current_value = float(current_card[1])
    update_status = db_bc_update_value(num, current_value + value)

    # close connection
    close_connection()

    return update_status

'''
return a tuple of a breezecard's info

:return
    a tuple of a breezecard's info
'''
def bc_info(num):
    # set up connection
    set_connection()

    # execute the query
    out = db_bc_info(num)

    # close connection
    close_connection()

    return out

'''
get a list of breezecard
'''
def get_bc_list(num = None, username = None, min_value = None, max_value = None):
    # set up connection
    set_connection()

    # execute the query
    out = db_bc_info(num, username, min_value, max_value)

    # close connection
    close_connection()

    return out

'''
generate a usable breezecard number

:return
    the generated bcn
'''
def generate_bc():
    # set up connection
    set_connection()

    # execute the query
    res = "%0.16d" % random.randint(0, 9999999999999999)
    bc_exist = db_bc_exist(res)
    if bc_exist == 0:
        # close connection
        close_connection()

        return res
    else:
        close_connection()
        generate_bc()



'''
return a list of all station's info
:return
    a list of tuples containing station brief info
    format:
    stopID, station_name, fare, status, istrain
    ('31955', 'Old Milton Pkwy - North Point Pkwy', Decimal('1.00'), 0, 0)
'''
def get_station_list():
    # set up connection
    set_connection()

    # execute the query
    out = db_station_retrieve()

    # close connection
    close_connection()

    return out

'''
return a tuple of a station's info

:return
    a tuple of a station's info
'''
def get_station_info(stopID):
    # set up connection
    set_connection()

    # execute the query
    out = db_station_retrieve(stopID)

    # close connection
    close_connection()

    return out

'''
return enterfare of station
'''
def get_station_fare(stopID):
    return float(station_info(stopID)[2])

'''
update the fare of station fare

:returns
    0 - successfully updated
    1 - any violation
'''
def station_update_fare(stopID, fare):
    # set up connection
    set_connection()

    # execute the query
    update_status = db_station_update_fare(stopID, fare)

    # close connection
    close_connection()

    return update_status

'''
insert a new station

returns
    0 - successfully updated
    1 - duplication key violation, StopID
    2 - any violation
'''
def insert_station(stopid, name, enterFare, ClosedStatus, isTrain):
    num = station_insert(stopid, name, enterFare, ClosedStatus, isTrain)
    return num

'''
return the passenger flow in a specific time span

format:
 stopNAME, Flow-in, Flow-out, Flow-net, Revenue
('Old Milton Pkwy - North Point Pkwy',   0,        0,        0,      0.0),
'''
def passenger_flow(startsTime=None, endsTime=None):
    # set up connection
    set_connection()
    # execute the query
    trips = db_trip_retrieve()
    stations = db_station_retrieve()
    # close connection
    close_connection()

    # initialize flow_in and flow-out
    station_id = [item[0] for item in stations]
    station_name = [item[1] for item in stations]
    respetive_name = {}
    flow_in = {}
    flow_out = {}
    for index in range(0, len(station_id)):
        respetive_name[station_id[index]] = station_name[index]
        flow_in[station_id[index]] = 0
        flow_out[station_id[index]] = 0

    # update flow_in and flow-out based on conditions
    if startsTime is None and endsTime is None:
        for t in trips:
            flow_in[t[-2]] += 1
            if t[-1] is not None:
                flow_out[t[-1]] += 1
    elif endsTime is None and startsTime is not None:
        for t in trips:
            if startsTime < str(t[1]):
                flow_in[t[-2]] += 1
                if t[-1] is not None:
                    flow_out[t[-1]] += 1
    else:
        for t in trips:
            if startsTime < str(t[1]) < endsTime:
                flow_in[t[-2]] += 1
                if t[-1] is not None:
                    flow_out[t[-1]] += 1

    # calculate flow_net and revenue based on flow_in and flow-out
    flow_net = {}
    revenue = {}
    for s in station_id:
        flow_net[s] = flow_in[s] - flow_out[s]
        fare = 0
        for i in stations:
            if i[0] == s:
                fare = float(i[2])
        revenue[s] = flow_in[s] * fare

    # put all together
    out = []
    for i in station_id:
        out.append((respetive_name[i], flow_in[i], flow_out[i], flow_net[i], revenue[i]))

    return tuple(out)

'''
return trip history in a specific time span

format:

'''
def trip_history(username):
    return 0

'''
returns
True: if user is in trip
        (True, (Decimal('1.00'), datetime.datetime(2017, 10, 31, 21, 30), '1325138309325420', 'FP', None))
False: if user is not in trip
        (False, None)
'''
def inTrip(username):
    # set up connection
    set_connection()

    # execute the query
    instance = db_user_inTrip(username)

    # close connection
    close_connection()

    return instance

'''
starting a trip

:returns
    0 - successfully started a trip
    1 - any violation
    2 - in a trip
'''
def take_trip(bcNum, startID):
    # set up connection
    set_connection()

    # execute the query


    # close connection
    close_connection()


'''
End the trip
'''
# def end_trip():
#     # TODO: ??
