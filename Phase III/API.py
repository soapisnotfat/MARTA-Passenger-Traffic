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
            conflict_insert(username, num, str(datetime.now())[:-7])
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
user delete breezecard
:returns
    0 - the card has been deleted
    other - any other violations
'''
def remove_breezecard(num):
    # set up connection
    set_connection()

    # execute the query
    status = db_bc_delete(num)

    # close connection
    close_connection()
    return status

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
    1000 - new value not satisfying constraint
    1 - any violation
'''
def bc_change_value(num, value):
    # check constraints
    if not 0 <= value <= 1000.00:
        # new value not satisfying constraint
        return 1000
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
    1000 - new value not satisfying constraint
    1 - any violation
'''
def bc_add_value(num, value):

    # set up connection
    set_connection()

    # execute the query
    current_card = db_bc_info(num)
    if current_card is None:
        return 1
    print current_card
    card = current_card[0]
    card_value = card[1]
    current_value = float(card_value)
    # check constraints
    if not 0 <= current_value + value <= 1000.00:
        # new value not satisfying constraint
        return 1000
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
def get_bc_list(num, username, min_value, max_value):
    # set up connection
    set_connection()

    # execute the query
    out = db_bc_info(num, username, min_value, max_value)

    # close connection
    close_connection()

    return tuple(out)

'''
return an unsuspended breezecard list

for User exclusively
'''
def bc_unsuspended_list(username):
    # set up connection
    set_connection()

    # execute the query
    temp = db_bc_info('', username, '', '')
    out = [item for item in temp if db_bc_is_suspended(item[0]) == 0]

    # close connection
    close_connection()

    return out

'''
remove current conflict from database
:returns
    0 - the conflict has been deleted
    other - any other violations
'''
def bc_remove_from_conflict(username, bcNum):
    # set up connection
    set_connection()

    # execute the query
    status = conflict_delete(username, bcNum)

    # close connection
    close_connection()

    return status

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
        # close connection
        close_connection()
        return generate_bc()

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
def station_fare(stopID):
    return float(get_station_info(stopID)[2])

'''
update the fare of station fare

:returns
    0 - successfully updated
    1000 - new fare not satisfying constraint
    1 - any violation
'''
def station_update_fare(stopID, fare):
    # check constraints
    if not 0 <= fare <= 50.00:
        # new fare not satisfying constraint
        return 1000
    # set up connection
    set_connection()

    # execute the query
    update_status = db_station_update_fare(stopID, fare)

    # close connection
    close_connection()

    return update_status

'''
update the closedStatus of station fare

:returns
    0 - successfully updated
    1 - any violation
'''
def station_update_closedstatus(stopID, status):
    # set up connection
    set_connection()

    # execute the query
    update_status = db_station_update_closedstatus(stopID, status)

    # close connection
    close_connection()

    return update_status

'''
insert a new station

returns
    0 - successfully inserted
    1 - duplication key violation, StopID
    1000 - new fare not satisfying constraint
    2 - any violation
'''
def insert_station(stopid, name, enterFare, ClosedStatus, isTrain, intersection=None):
    # check constraints
    if not 0 <= enterFare <= 50.00:
        # new fare not satisfying constraint
        return 1000
    # set up connection
    set_connection()

    if isTrain == 1:
        status = station_insert(stopid, name, enterFare, ClosedStatus, isTrain)
        # close connection
        close_connection()
        return status
    else:
        status = station_insert(stopid, name, enterFare, ClosedStatus, isTrain)
        if status != 0:
            # close connection
            close_connection()
            return status
        else:
            intersection_insertion = busStationIntersection_insert(stopid, intersection)
            if intersection_insertion != 0:
                station_delete(stopid)
                # close connection
                close_connection()
            return intersection_insertion

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
return all conflicts

format:
        bcNum,       new owner,    conflict date,     previous owner
('4769432303280540', 'kellis', '2017-10-23 16:21:49', 'sandrapatel'),
('4769432303280540', 'riyoy1996', '2017-10-23 16:21:49', 'sandrapatel'),
('0475861680208144', 'sandrapatel', '2018-11-12 00:00:01', 'commuter14')

'''
def conflict_list():
    # set up connection
    set_connection()

    conflicts = db_conflict_retrieve()
    out = []
    for c in conflicts:
        temp = [c[0], c[1], str(c[2]), c[3]]
        out.append(tuple(temp))

    # close connection
    close_connection()

    return tuple(out)

'''
return trip history in a specific time span

format:
        time           source dst   fare        num
['2017-10-31 21:30:00', 'FP', None, 1.0, '1325138309325420'],
['2017-10-28 22:11:13', 'N4', 'N11', 1.5, '9248324548250130']

'''
def trip_history(username, startTime=None, endTime=None):
    # set up connection
    set_connection()

    stations = db_station_retrieve()
    station_id = [item[0] for item in stations]
    station_name = [item[1] for item in stations]
    respective_name = {}
    for index in range(0, len(station_id)):
        respective_name[station_id[index]] = station_name[index]

    BCs = db_user_bc_num(username)
    trips = []
    for bc in BCs:
        for trip in db_trip_retrieve(bc):
            trips.append(trip)

    # close connection
    close_connection()
    out_list = []
    for t in trips:
        if t[4]:
            out_list.append(tuple([str(t[1]), respetive_name[t[3]], respetive_name[t[4]], float(t[0]), t[2]]))

        else:
            out_list.append(tuple([str(t[1]), respetive_name[t[3]], "None", float(t[0]), t[2]]))
    out = tuple(out_list)
    return out

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
    97 - station has been closed
    98 - current card is suspended
    99 - fare deduction failed
    other - any violation
'''
def take_trip(bcNum, startID):
    # set up connection
    set_connection()

    # execute the query
    start_station = db_station_retrieve(startID)

    if start_station[-2] == 1:
        # station has been closed
        return 97

    suspension_status = db_bc_is_suspended(bcNum)
    if suspension_status != 0:
        # current card is suspended
        return 98

    fare = float(start_station[2])
    deduction_status = db_bc_deduct_value(bcNum, fare)
    if deduction_status != 0:
        # not enough balance to take this trip
        return 99

    time = str(datetime.now())[:-7]
    status = trip_insert(fare, time, bcNum, startID)

    # close connection
    close_connection()

    return status

'''
End the trip

:returns
    0 - is not in trip
    1 - end trip successfully
'''
def end_trip(username, endId):
    current_trip = inTrip(username)
    if not current_trip[0]:
        return 0
    trip_detail = current_trip[1]
    # set up connection
    set_connection()

    # execute the query
    time = str(trip_detail[1])
    bcNum = trip_detail[2]
    status = db_trip_update(time, bcNum, endId)

    # close connection
    close_connection()

    return status
