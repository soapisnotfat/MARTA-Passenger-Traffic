from datetime import datetime
import pymysql
import traceback


# Global variables
_connected = False
_database = None
_cursor = None

'''
database connection managements
'''
def set_connection():
    global _connected
    global _database
    global _cursor

    if not _connected:
        try:
            print("********************************************")
            print("*          Prepare for connection          *")

            _database = pymysql.connect(host="academic-mysql.cc.gatech.edu",
                                        user="cs4400_Group_91",
                                        passwd="_OY4gwQs",
                                        db="cs4400_Group_91")

            print("*    Connections should be ready to go     *")
            _cursor = _database.cursor()
            _connected = True
            if _connected:
                print("*            Connections Setup             *")
            else:
                print("*            Connections FAIL              *")
            print("********************************************\n")

        except Exception as e:
            _connected = False
            traceback.print_exc()

def close_connection():
    global _connected

    if _connected:
        _database.close()
        _connected = False
    print("********************************************\n" +
          "*            Connections Closed            *\n" +
          "********************************************\n")


'''
BASE LAYER FUNCTIONS providing service for upper lay functions
'''

# function that check if user is an admin
#
# returns:
#   0 - is not
#   1 - is
def db_user_isAdmin(username):
    query = "SELECT IsAdmin FROM User WHERE Username = '%s'"
    response = _cursor.execute(query % username)

    return _cursor.fetchall()[0][0]

# login function that check the login status
#
# returns:
#     case 0 for failed tries
#     case 1 for administrator login
#     case 2 for passenger login
def db_login(username, password):
    query = "SELECT * FROM User WHERE Username = '%s'AND Password = '%s'"
    response = _cursor.execute(query % (username, password))

    # clear cursor
    _cursor.fetchall()

    if response == 0:
        return 0
    else:
        query = "SELECT IsAdmin FROM User WHERE Username = '%s'"
        _cursor.execute(query % username)

        result = _cursor.fetchone()

        # sanity check
        _cursor.fetchall()

        if result[0] == 1:
            return 1
        else:
            return 2

# returns:
#   0 - doesn't exist
#   1 - exist
def db_bc_exist(num):
    query = "SELECT * FROM Breezecard WHERE breezecardNum = '%s'"
    response = _cursor.execute(query % num)
    _cursor.fetchall()
    if response == 0:
        return 0
    else:
        return 1

# returns:
#   the info of this card
#   format: ('0919948381768459', Decimal('126.50'), 'commuter14')
#           ('9876543212345670', Decimal('92.50'), None)
def db_bc_info(num, username, min_value, max_value):
    if num == "" \
            and username == "" \
            and min_value == "" \
            and max_value == "":
        # if num is None:
        query = "SELECT * FROM Breezecard ORDER BY BreezecardNum ASC"
        _cursor.execute(query)
        res = _cursor.fetchall()
        return res
    elif num != "" \
            and username == "" \
            and min_value == "" \
            and max_value == "":
        query = "SELECT * FROM Breezecard WHERE BreezecardNum = '%s' ORDER BY BreezecardNum ASC"
        _cursor.execute(query % num)
        res = _cursor.fetchall()
        return res
    elif num == "" \
            and username != "" \
            and min_value == "" \
            and max_value == "":
        query = "SELECT * FROM Breezecard WHERE BelongsTo = '%s' ORDER BY BreezecardNum ASC"
        _cursor.execute(query % username)
        res = _cursor.fetchall()
        return res
    elif num != "" \
            and username != "" \
            and min_value == "" \
            and max_value == "":
        query = "SELECT * FROM Breezecard WHERE BelongsTo = '%s' AND BreezecardNum = '%s' ORDER BY BreezecardNum ASC"
        _cursor.execute(query % (username, num))
        res = _cursor.fetchall()
        return res

    elif num == "" \
            and username == "" \
            and min_value != "" \
            and max_value != "":
        query = "SELECT * FROM Breezecard WHERE '%s' <= Value AND Value <= '%s' ORDER BY BreezecardNum ASC"
        _cursor.execute(query % (min_value, max_value))
        res = _cursor.fetchall()
        return res
    elif num != "" \
            and username == "" \
            and min_value != "" \
            and max_value != "":
        query = "SELECT * FROM Breezecard WHERE BreezecardNum = '%s' AND '%s' <= Value AND Value <= '%s' ORDER BY BreezecardNum ASC"
        _cursor.execute(query % (num, min_value, max_value))
        res = _cursor.fetchall()
        return res
    elif num == "" \
            and username != "" \
            and min_value != "" \
            and max_value != "":
        query = "SELECT * FROM Breezecard WHERE BelongsTo = '%s' AND '%s' <= Value AND Value <= '%s' ORDER BY BreezecardNum ASC"
        _cursor.execute(query % (username, min_value, max_value))
        res = _cursor.fetchall()
        return res
    elif num != "" \
            and username != "" \
            and min_value != "" \
            and max_value != "":
        query = "SELECT * FROM Breezecard WHERE BreezecardNum = '%s' AND BelongsTo = '%s' AND '%s' <= Value AND Value <= '%s' ORDER BY BreezecardNum ASC"
        _cursor.execute(query % (num, username, min_value, max_value))
        res = _cursor.fetchall()
        return res

    elif num == "" \
            and username == "" \
            and min_value != "" \
            and max_value == "":
        query = "SELECT * FROM Breezecard WHERE '%s' <= Value ORDER BY BreezecardNum ASC"
        _cursor.execute(query % min_value)
        res = _cursor.fetchall()
        return res
    elif num != "" \
            and username == "" \
            and min_value != "" \
            and max_value == "":
        query = "SELECT * FROM Breezecard WHERE BreezecardNum = '%s' AND '%s' <= Value ORDER BY BreezecardNum ASC"
        _cursor.execute(query % (num, min_value))
        res = _cursor.fetchall()
        return res
    elif num == "" \
            and username != "" \
            and min_value != "" \
            and max_value == "":
        query = "SELECT * FROM Breezecard WHERE BelongsTo = '%s' AND '%s' <= Value ORDER BY BreezecardNum ASC"
        _cursor.execute(query % (username, min_value))
        res = _cursor.fetchall()
        return res
    elif num != "" \
            and username != "" \
            and min_value != "" \
            and max_value == "":
        query = "SELECT * FROM Breezecard WHERE BreezecardNum = '%s' AND BelongsTo = '%s' AND '%s' <= Value ORDER BY BreezecardNum ASC"
        _cursor.execute(query % (num, username, min_value))
        res = _cursor.fetchall()
        return res

    elif num == "" \
            and username == "" \
            and min_value == "" \
            and max_value != "":
        query = "SELECT * FROM Breezecard WHERE Value <= '%s' ORDER BY BreezecardNum ASC"
        _cursor.execute(query % max_value)
        res = _cursor.fetchall()
        return res
    elif num != "" \
            and username == "" \
            and min_value == "" \
            and max_value != "":
        query = "SELECT * FROM Breezecard WHERE BreezecardNum = '%s' AND Value <= '%s' ORDER BY BreezecardNum ASC"
        _cursor.execute(query % (num, max_value))
        res = _cursor.fetchall()
        return res
    elif num == "" \
            and username != "" \
            and min_value == "" \
            and max_value != "":
        query = "SELECT * FROM Breezecard WHERE BelongsTo = '%s' AND Value <= '%s' ORDER BY BreezecardNum ASC"
        _cursor.execute(query % (username, max_value))
        res = _cursor.fetchall()
        return res
    elif num != "" \
            and username != "" \
            and min_value == "" \
            and max_value != "":
        query = "SELECT * FROM Breezecard WHERE BreezecardNum = '%s' AND BelongsTo = '%s' AND Value <= '%s' ORDER BY BreezecardNum ASC"
        _cursor.execute(query % (num, username, max_value))
        res = _cursor.fetchall()
        return res

# returns
#   the bcNum of one user
def db_user_bc_num(username):
    out = [list(item)[0] for item in db_bc_info('', username, '', '')]
    return out

# returns
# True: if user is in trip
#     (True, (Decimal('1.00'), datetime.datetime(2017, 10, 31, 21, 30), '1325138309325420', 'FP', None))
# False: if user is not in trip
#     (False, None)
def db_user_inTrip(username):
    out = [list(item)[0] for item in db_bc_info('', username, '', '')]
    for num in out:
        info = db_trip_retrieve(num)
        for trip in info:
            if trip[-1] is None:
                return True, trip
    return False, None

# insert tuples to user
# @param: String: username
# @param: String: Password
# @param: int: isAdmin (1 or 0) ---- this is aborted
# returns:
#   0 - successfully inserted
#   1 - primary key violation
#   2 - other violations
def user_insert(username, password, isAdmin=None):
    if isAdmin is None:
        query = "INSERT INTO User(Username, Password, IsAdmin) VALUES ('%s', '%s', '%d');"
        try:
            print("log :: executing user insertion query\n")
            _cursor.execute(query % (username, password, 0))
            _database.commit()
            print("++ Successfully insert " + username + " into database ++\n")
            return 0

        except Exception as e:
            print("---> run into Exception:")
            print("---> " + str(e) + '\n')  # print exception message
            if str(e)[1:5] == "1062":
                # violates primary key constraint, username
                return 1
            else:
                # other violation
                return 2

# delete tuples from user
# @param: String: Username
# returns:
#   0 - successfully deleted
#   1 - deletion failed
def user_delete(username):
    query = "DELETE FROM User WHERE Username = '%s';"
    try:
        print("log :: executing user deletion query\n")
        _cursor.execute(query % username)
        _database.commit()
        print("++ Successfully delete " + username + " from database ++\n")
        return 0

    except Exception as e:
        print("---> run into Exception:")
        print("---> " + str(e) + '\n')  # print exception message
        return 1

# insert tuple to user
# @param: String: username
# @param: String: email
# returns:
#   0 - successfully inserted
#   1 - primary key violation
#   2 - other violation
def passenger_insert(username, email):
    query = "INSERT INTO Passenger(Username, Email) VALUES ('%s', '%s')"
    try:
        print("log :: executing passenger insertion query\n")
        _cursor.execute(query % (username, email))
        _database.commit()
        print("++ Successfully insert " + username + " into database ++\n")
        return 0

    except Exception as e:
        print("---> run into Exception:")
        print("---> " + str(e) + '\n')  # print exception message
        if str(e)[1:5] == "1062":
            # primary key violation: Email
            return 1
        else:
            # other violations
            return 2

# insert tuples to Breezecard
# @param: String: num (length 16 fixed)
# @param: int: value
# @param: String: BelongsTO
# returns:
#   0 - successfully inserted
#   1 - primary key violation
#   2 - foreign key violation
def bc_insert(num, value, BelongsTo=None):
    if BelongsTo is None:
        query = "INSERT INTO Breezecard(BreezecardNum, Value) VALUES ('%s', '%f')"
        try:
            print("log :: executing Breezecard insertion query\n")
            _cursor.execute(query % (num, value))
            _database.commit()
            print("++ Successfully insert " + num + " into database ++\n")
            return 0

        except Exception as e:
            print("---> run into Exception:")
            print("---> " + str(e) + '\n')  # print exception message
            error = str(e)[1:5]
            if error == "1062":
                # primary key violation, breezecardNum
                return 1
            elif error == "1452":
                # foreign key violation, BelongsTo
                return 2

    else:
        query = "INSERT INTO Breezecard(BreezecardNum, Value, BelongsTO) VALUES ('%s', '%f', '%s')"
        try:
            print("log :: executing Breezecard insertion query\n")
            _cursor.execute(query % (num, value, BelongsTo))
            _database.commit()
            print("++ Successfully insert " + num + " into database ++\n")
            return 0

        except Exception as e:
            print("---> run into Exception:")
            print("---> " + str(e) + '\n')  # print exception message
            error = str(e)[1:5]
            if error == "1062":
                # primary key violation, breezecardNum
                return 1
            elif error == "1452":
                # foreign key violation, BelongsTo
                return 2

# update breezecard value given breezecard num
# @param: String: num (length 16 fixed)
# @param: int: value
# returns:
#   0 - successfully updated
#   1 - any exception
def db_bc_update_value(num, value):
    query = "UPDATE Breezecard SET Value = '%f' WHERE BreezecardNum = '%s'"
    try:
        print("log :: executing Breezecard update query\n")
        _cursor.execute(query % (value, num))
        _database.commit()
        print("++ Successfully update " + num + "'s value ++\n")
        return 0

    except Exception as e:
        print("---> run into Exception:")
        print("---> " + str(e) + '\n')  # print exception message
        return 1

# update breezecard holder given breezecard num
# @param: String: num (length 16 fixed)
# @param: String: BelongsTo
# returns:
#   0 - successfully updated
#   1 - any exception
def db_bc_update_holder(num, username=None):
    if username is None:
        query = "UPDATE Breezecard SET BelongsTo = NULL WHERE BreezecardNum = '%s'"
        try:
            print("log :: executing Breezecard update query\n")
            _cursor.execute(query % num)
            _database.commit()
            print("++ Successfully update " + num + "'s holder ++\n")
            return 0

        except Exception as e:
            print("---> run into Exception:")
            print("---> " + str(e) + '\n')  # print exception message
            return 1
    else:
        query = "UPDATE Breezecard SET BelongsTo = '%s' WHERE BreezecardNum = '%s'"
        try:
            print("log :: executing Breezecard update query\n")
            _cursor.execute(query % (username, num))
            _database.commit()
            print("++ Successfully update " + num + "'s holder ++\n")
            return 0

        except Exception as e:
            print("---> run into Exception:")
            print("---> " + str(e) + '\n')  # print exception message
            return 1

# check is given bc is suspended
# @param: String: num (length 16 fixed)
# returns:
#   0 - not suspended
#   1 - suspended
def db_bc_is_suspended(num):
    status = db_conflict_retrieve(num)
    if len(status) == 0 or status is None:
        return 0
    else:
        return 1

# delete tuples from breezecard
# @param: String: breezecardNum
# returns:
#   0 - successfully deleted
#   1 - deletion failed
def db_bc_delete(num):
    query = "DELETE FROM Breezecard WHERE BreezecardNum = '%s';"
    try:
        print("log :: executing breezecard deletion query\n")
        _cursor.execute(query % num)
        _database.commit()
        print("++ Successfully delete " + num + " from database ++\n")
        return 0

    except Exception as e:
        print("---> run into Exception:")
        print("---> " + str(e) + '\n')  # print exception message
        return 1

# insert tuples to Station
# @param: String: StopID
# @param: String: Name
# @param: int: EnterFare
# @param: int: CloseStatus (0 or 1)
# @param: int: IsTrain (1 or 0)
# returns:
#   0 - successfully inserted
#   1 - duplication key violation, StopID
#   2 - any violation
def station_insert(stopid, name, enterFare, ClosedStatus, isTrain):
    query = "INSERT INTO Station(StopID, Name, EnterFare, ClosedStatus, IsTrain) VALUES ('%s', '%s', '%f', '%d', '%d')"
    try:
        print("log :: executing station insertion query\n")
        _cursor.execute(query % (stopid, name, enterFare, ClosedStatus, isTrain))
        _database.commit()
        print("++ Successfully insert " + stopid + " into database++\n")
        return 0

    except Exception as e:
        print("---> run into Exception:")
        print("---> " + str(e) + '\n')  # print exception message
        error = str(e)[1:5]
        if error == "1062":
            # duplication key violation, StopID / Name&IsTrain
            return 1
        else:
            # other violations
            return 2

# delete tuples from station
# @param: String: stopID
# returns:
#   0 - successfully deleted
#   1 - deletion failed
def station_delete(stopID):
    query = "DELETE FROM Station WHERE StopID = '%s';"
    try:
        print("log :: executing statoion deletion query\n")
        _cursor.execute(query % stopID)
        _database.commit()
        print("++ Successfully delete " + stopID + " from database ++\n")
        return 0

    except Exception as e:
        print("---> run into Exception:")
        print("---> " + str(e) + '\n')  # print exception message
        return 1

# retrieve station info
#
# returns
#     a tuple of one station's info
#     a tuple of tuples of stations' info
# format: ('N4', 'Midtown', Decimal('5.00'), 0, 1, None)
def db_station_retrieve(stopID=None, openStatus=None):
    if stopID is None:
        if openStatus is None:
            query = "SELECT S.*, B.Intersection FROM Station S LEFT JOIN BusStationIntersection B ON S.StopID = B.StopID ORDER BY StopID"
            _cursor.execute(query)
            res = _cursor.fetchall()
            return res
        else:
            query = "SELECT S.*, B.Intersection FROM Station S LEFT JOIN BusStationIntersection B ON S.StopID = B.StopID WHERE S.ClosedStatus = 0 ORDER BY StopID"
            _cursor.execute(query)
            res = _cursor.fetchall()
            return res
    else:
        if openStatus is None:
            query = "SELECT S.*, B.Intersection FROM (Station S LEFT JOIN BusStationIntersection B ON S.StopID = B.StopID) WHERE S.StopID = '%s'"
            _cursor.execute(query % stopID)
            res = _cursor.fetchone()
            _cursor.fetchall()
            return res
        else:
            query = "SELECT S.*, B.Intersection FROM Station S LEFT JOIN BusStationIntersection B ON S.StopID = B.StopID WHERE S.ClosedStatus = 0 AND S.StopID = '%s'"
            _cursor.execute(query)
            res = _cursor.fetchall()
            return res

# update the enter fare of a station
#
# returns
#   0 - successfully updated
#   1 - any violation
def db_station_update_fare(stopID, fare):
    query = "UPDATE Station SET EnterFare = '%f' WHERE StopID = '%s'"
    try:
        print("log :: executing Station update query\n")
        _cursor.execute(query % (fare, stopID))
        _database.commit()
        print("++ Successfully update " + stopID + "'s fare ++\n")
        return 0

    except Exception as e:
        print("---> run into Exception:")
        print("---> " + str(e) + '\n')  # print exception message
        return 1

# update the closeStatus of a station
#
# returns
#   0 - successfully updated
#   1 - any violation
def db_station_update_closedstatus(stopID, ClosedStatus):
    query = "UPDATE Station SET ClosedStatus = '%d' WHERE StopID = '%s'"
    try:
        print("log :: executing Station update query\n")
        _cursor.execute(query % (ClosedStatus, stopID))
        _database.commit()
        print("++ Successfully update " + stopID + "'s fare ++\n")
        return 0

    except Exception as e:
        print("---> run into Exception:")
        print("---> " + str(e) + '\n')  # print exception message
        return 1

# insert tuples to busStation
# @param: String: StopID
# @param: String: Intersection
# returns:
#   0 - successfully inserted
#   1 - duplication key violation, StopID
#   2 - other violation
def busStationIntersection_insert(stopid, intersection=None):
    if intersection is None:
        query = "INSERT INTO BusStationIntersection(StopID) VALUES ('%s')"
        try:
            print("log :: executing busStation insertion query\n")
            _cursor.execute(query % stopid)
            _database.commit()
            print("++ Successfully insert " + stopid + " into database++\n")
            return 0

        except Exception as e:
            print("---> run into Exception:")
            print("---> " + str(e) + '\n')  # print exception message
            error = str(e)[1:5]
            if error == "1062":
                # duplication key violation, StopID
                return 1
            else:
                # other violations
                return 2
    else:
        query = "INSERT INTO BusStationIntersection(StopID, Intersection) VALUES ('%s', '%s')"
        try:
            print("log :: executing busStation insertion query\n")
            _cursor.execute(query % (stopid, intersection))
            _database.commit()
            print("++ Successfully insert " + stopid + " into database++\n")
            return 0

        except Exception as e:
            print("---> run into Exception:")
            print("---> " + str(e) + '\n')  # print exception message
            error = str(e)[1:5]
            if error == "1062":
                # duplication key violation, StopID
                return 1
            else:
                # other violation
                return 2

# retrieve intersection info
#
# returns
#     a tuple of one station's info
#     a tuple of tuples of stations' info
# format: ('31955', 'Old Milton Pkwy - North Point Pkwy', Decimal('1.00'), 0, 0)
def intersection_retrieve(stopID=None):
    if stopID is None:
        query = "SELECT * FROM BusStationIntersection ORDER BY StopID"
        _cursor.execute(query)
        res = _cursor.fetchall()
        return res
    else:
        query = "SELECT * FROM BusStationIntersection WHERE StopID = '%s'"
        _cursor.execute(query % stopID)
        res = _cursor.fetchone()
        res = res[1]
        _cursor.fetchall()
        return res

# insert tuples to Conflict
# @param: String: Username
# @param: String: BreezecardNum
# @param: String: Datetime
#   0 - successfully inserted
#   1 - duplication key violation
#   2 - other violation
def conflict_insert(username, BreezeCardNum, DateAndTime):
    query = "INSERT INTO Conflict(Username, BreezecardNum, DateAndTime) VALUES ('%s', '%s', '%s')"
    try:
        print("log :: executing conflict insertion query\n")
        _cursor.execute(query % (username, BreezeCardNum, DateAndTime))
        _database.commit()
        print("++ Successfully insert " + username + " into database++\n")
        return 0

    except Exception as e:
        print("---> run into Exception:")
        print("---> " + str(e) + '\n')  # print exception message
        error = str(e)[1:5]
        if error == "1062":
            # duplication key violation
            return 1
        else:
            # other violations
            return 2

# delete tuples from conflict
# @param: String: username
# @param: String: BreezeCardNum
# returns:
#   0 - successfully deleted
#   1 - deletion failed
def conflict_delete(username, bcNum):
    query = "DELETE FROM Conflict WHERE Username = '%s' and BreezecardNum = '%s'"
    try:
        print("log :: executing conflict deletion query\n")
        _cursor.execute(query % (username, bcNum))
        _database.commit()
        print("++ Successfully delete " + bcNum + " from database ++\n")
        return 0

    except Exception as e:
        print("---> run into Exception:")
        print("---> " + str(e) + '\n')  # print exception message
        return 1

# retrieve Conflict info
#
# returns
#     a tuple of one Conflict's info
#     a tuple of tuples of Conflict' info
# format: ('31955', 'Old Milton Pkwy - North Point Pkwy', Decimal('1.00'), 0, 0)
def db_conflict_retrieve(num=None):
    if num is None:
        query = "SELECT C.BreezecardNum, C.Username, C.DateAndTime, B.BelongsTo FROM Conflict C LEFT JOIN Breezecard B On C.BreezecardNum = B.BreezecardNum ORDER BY BreezecardNum"
        _cursor.execute(query)
        res = _cursor.fetchall()
        return res
    else:
        query = "SELECT C.BreezecardNum, C.Username, C.DateAndTime, B.BelongsTo FROM Conflict C LEFT JOIN Breezecard B On C.BreezecardNum = B.BreezecardNum WHERE C.BreezecardNum = '%s' ORDER BY BreezecardNum"
        _cursor.execute(query % num)
        res = _cursor.fetchall()
        return res

# insert tuples to Trip
# @param: float: Tripfare
# @param: String: StartTime
# @param: String: BreezecardNum
# @param: String: StartsAt
# @param: String: EndsAt
#   0 - successfully inserted
#   1 - duplication key violation
#   2 - other violation
def trip_insert(Tripfare, StartTime, BreezecardNum, StartsAt, EndsAt=None):
    if EndsAt is None:
        query = "INSERT INTO Trip(Tripfare, StartTime, BreezecardNum, StartsAt) VALUES ('%f', '%s', '%s', '%s')"
        try:
            print("log :: executing trip insertion query\n")
            _cursor.execute(query % (Tripfare, StartTime, BreezecardNum, StartsAt))
            _database.commit()
            print("++ Successfully insert " + BreezecardNum + " into database++\n")
            return 0

        except Exception as e:
            print("---> run into Exception:")
            print("---> " + str(e) + '\n')  # print exception message
            error = str(e)[1:5]
            if error == "1062":
                # duplication key violation
                return 1
            else:
                # other violations
                return 2
    else:
        query = "INSERT INTO Trip(Tripfare, StartTime, BreezecardNum, StartsAt, EndsAt) VALUES ('%f', '%s', '%s', '%s', '%s')"
        try:
            print("log :: executing trip insertion query\n")
            _cursor.execute(query % (Tripfare, StartTime, BreezecardNum, StartsAt, EndsAt))
            _database.commit()
            print("++ Successfully insert " + BreezecardNum + " into database++\n")
            return 0

        except Exception as e:
            print("---> run into Exception:")
            print("---> " + str(e) + '\n')  # print exception message
            error = str(e)[1:5]
            if error == "1062":
                # duplication key violation
                return 1
            else:
                # other violations
                return 2

# update trip's destination
# @param: String: time
# @param: String: bcNum (length 16 fixed)
# @param: String: endsID
# returns:
#   0 - successfully updated
#   1 - any exception
def db_trip_update(time, bcNum, endsID):
    query = "UPDATE Trip SET EndsAt = '%s' WHERE StartTime = '%s' AND BreezecardNum = '%s'"
    try:
        print("log :: executing trip update query\n")
        _cursor.execute(query % (endsID, time, bcNum))
        _database.commit()
        print("++ Successfully update " + bcNum + "'s holder ++\n")
        return 0

    except Exception as e:
        print("---> run into Exception:")
        print("---> " + str(e) + '\n')  # print exception message
        return 1

# retrieve Trip info
#
# returns
#   a tuple of one trip's info
#   a tuple of tuples of station's info
def db_trip_retrieve(bcNum=None, startTime=None, endTime=None):
    if bcNum is None:
        if startTime is None and endTime is None:
            query = "SELECT * FROM Trip ORDER BY StartTime"
            _cursor.execute(query)
            res = _cursor.fetchall()
            return res
        elif endTime is not None and startTime is None:
            query = "SELECT * FROM Trip WHERE StartTime <= '%s' ORDER BY StartTime"
            _cursor.execute(query % endTime)
            res = _cursor.fetchall()
            return res
        elif startTime is not None and endTime is None:
            query = "SELECT * FROM Trip WHERE StartTime >= '%s' ORDER BY StartTime"
            _cursor.execute(query % startTime)
            res = _cursor.fetchall()
            return res
        else:
            query = "SELECT * FROM Trip WHERE StartTime >= '%s' AND StartTime <= '%s' ORDER BY StartTime"
            _cursor.execute(query % (startTime, endTime))
            res = _cursor.fetchall()
            return res

    else:
        if startTime is None and endTime is None:
            query = "SELECT * FROM Trip WHERE BreezecardNum = '%s' ORDER BY StartTime"
            _cursor.execute(query % bcNum)
            res = _cursor.fetchall()
            return res
        elif endTime is not None and startTime is None:
            query = "SELECT * FROM Trip WHERE BreezecardNum = '%s' AND StartTime <= '%s' ORDER BY StartTime"
            _cursor.execute(query % (bcNum, endTime))
            res = _cursor.fetchall()
            return res
        elif startTime is not None and endTime is None:
            query = "SELECT * FROM Trip WHERE BreezecardNum = '%s' AND StartTime >= '%s' ORDER BY StartTime"
            _cursor.execute(query % (bcNum, startTime))
            res = _cursor.fetchall()
            return res
        else:
            query = "SELECT * FROM Trip WHERE BreezecardNum = '%s' AND StartTime >= '%s' AND StartTime <= '%s' ORDER BY StartTime"
            _cursor.execute(query % (bcNum, startTime, endTime))
            res = _cursor.fetchall()
            return res
