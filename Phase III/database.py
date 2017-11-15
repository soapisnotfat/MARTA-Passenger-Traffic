# from datetime import datetime
import pymysql
import re
import traceback


# Global variables
_connected = False
_database = None
_cursor = None

# setups - ignore this section
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


def turnoff_connection():
    global _connected

    if _connected:
        _database.close()
        _connected = False
    print("********************************************\n" +
          "*            Connections Closed            *\n" +
          "********************************************\n")




'''
UPPER LAYER FUNCTION

- IMPORTANCE-: 
    - only use functions in this section for front-end implementation
    - follow the documentation of each function
'''

# register function that inserts tuples to database
#
# returns:
#     case 0 for register successfully
#     case 1 for email doesn't match format
#     case 2 for username duplication
#     case 3 for email duplication
#     case 4 for all other exceptions
def register(username, password, email, isAdmin):
    user_insert_result = user_insert(username, password, isAdmin)
    if user_insert_result == "username duplication":
        return 2
    elif user_insert_result == "user other exception":
        return 4
    if not isAdmin:
        passenger_insert_result = passenger_insert(username, email)
        if passenger_insert_result == "email format not match":
            return 1
        elif passenger_insert_result == "email duplication":
            user_delete(username)
            return 3
    return 0


# login function that check the login status
#
# returns:
#     case 0 for failed tries
#     case 1 for administrator login
#     case 2 for passenger login
def login(username, password):
    query = "SELECT * FROM User WHERE Username = %s AND Password = %s"
    response = _cursor.execute(query, (username, password))

    # clear cursor
    _cursor.fetchall()

    if response == 0:
        return 0
    else:
        query = "SELECT IsAdmin FROM User WHERE Username = %s"
        _cursor.execute(query, username)

        result = _cursor.fetchone()

        # sanity check
        _cursor.fetchall()

        if result[0] == 1:
            return 1
        else:
            return 2





'''
INNER LAYER FUNCTIONS providing service for upper lay functions

- DO NOT MODIFY THIS SECTION -
'''

# insert tuples to user
# @param: String: username
# @param: String: Password
# @param: int: isAdmin (1 or 0) ---- this is aborted
# returns:
#   0 - successfully inserted
#   1 - primary key violation
#   2 - other violations
def user_insert(username, password):
    query = "INSERT INTO User(Username, Password, IsAdmin) VALUES ('%s', '%s', '%d');"
    try:
        print("log :: executing user insertion query\n")
        _cursor.execute(query % (username, password, 0))
        _database.commit()
        print("++ Successfully insert " + username + " into database ++\n")
        return 0

    except Exception as e:
        print("----------------------------\n" +
              "---> run into Exception <---\n" +
              "----------------------------")
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
        print("----------------------------\n" +
              "---> run into Exception <---\n" +
              "----------------------------")
        print("---> " + str(e) + '\n')  # print exception message
        return 1


# insert tuple to user
# @param: String: username
# @param: String: email
# returns:
#   -1 - email format doesn't match
#   0 - successfully inserted
#   1 - deletion failed
def passenger_insert(username, email):
    email_regex = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if not email_regex.match(email):
        return -1

    query = "INSERT INTO Passenger(Username, Email) VALUES ('%s', '%s')"
    try:
        print("log :: executing passenger insertion query\n")
        _cursor.execute(query % (username, email))
        _database.commit()
        print("++ Successfully insert " + username + " into database ++\n")
        return 0

    except Exception as e:
        print("----------------------------\n" +
              "---> run into Exception <---\n" +
              "----------------------------")
        print("---> " + str(e) + '\n')  # print exception message
        if str(e)[1:5] == "1062":
            # primary key violation: Email
            return 1


# insert tuples to Breezecard
# @param: String: num (length 16 fixed)
# @param: int: value
# @param: String: BelongsTO
def breezecard_insert(num, value, BelongsTo):
    query = "INSERT INTO Breezecard(BreezecardNum, Value, BelongsTo) VALUES ('%s', '%d', '%s')"
    try:
        print("log :: executing Breezecard insertion query\n")
        _cursor.execute(query % (num, value, BelongsTo))
        _database.commit()
        print("++ Successfully insert " + num + " into database ++\n")
        return 0

    except Exception as e:
        print("----------------------------\n" +
              "---> run into Exception <---\n" +
              "----------------------------")
        print("---> " + str(e) + '\n')  # print exception message
        if str(e)[1:5] == "1062":
            # primary key violation, breezecardNum
            return 1


# update breezecard value given breezecard num
# @param: String: num (length 16 fixed)
# @param: int: value
def breezecard_update_value(num, value):
    query = "UPDATE Breezecard SET Value = %d WHERE BreezecardNum = %s"
    try:
        _cursor.execute(query, (value, num))
        _database.commit()
    except Exception as e:
        # TODO: see if some condition will break this query
        return ""


# insert tuples to Station
# @param: String: StopID
# @param: String: Name
# @param: int: EnterFare
# @param: int: CloseStatus (0 or 1)
# @param: int: IsTrain (1 or 0)
def staion_insert(stopid, name, enterFare, ClosedStatus, isTrain):
    query = "INSERT INTO Station(StopID, Name, EnterFare, ClosedStatus, IsTrain) VALUES (%s, %s, %d, %d, %d)"
    try:
        _cursor.execute(query, (stopid, name, enterFare, ClosedStatus, isTrain))
        _database.commit()
    except Exception as e:
        if True:
            # TODO: find the duplication condition
            return "StopID duplication"
        elif True:
            # TODO: find name and isTrain uniqueness violation condition
            return "Name and IsTrain uniqueness violation"


def busStationIntersection_insert(stopid, intersection):
    query = "INSERT INTO BusStationIntersection(StopID, Intersection) VALUES (%s, %s)"
    try:
        _cursor.execute(query, (stopid, intersection))
        _database.commit()
    except Exception as e:
        if True:
            # TODO: find the duplication condition
            return "StopID duplication"


# insert tuples to Conflict
# @param: String: Username
# @param: String: BreezecardNum
# @param: String: Datetime
def conflict_insert(username, BreezeCardNum, DateTime):
    # TODO: check the instance of TimeStamp
    query = "INSERT INTO Conflict(Username, BreezecardNum, DataTime) VALUES (%s, %s, %s)"
    try:
        _cursor.execute(query, (username, BreezeCardNum, DateTime))
        _database.commit()
    except Exception as e:
        if True:
            # TODO: find the duplication condition
            return "Username or BreezecardNum duplication"

# insert tuples to Trip
# @param: int: Tripfare
# @param: String: StartTime
# @param: String: BreezecardNum
# @param: String: StartsAt
def trip_insert(Tripfare, StartTime, BreezecardNum, StartsAt):
    # TODO: check the instance of TimeStamp
    query = "INSERT INTO Trip(Tripfare, StartTime, BreezecardNum, StartsAt) VALUES (%d, %s, %s, %s)"
    try:
        _cursor.execute(query, (Tripfare, StartTime, BreezecardNum, StartsAt))
        _database.commit()
    except Exception as e:
        if True:
            # TODO: find the duplication condition
            return "StartTime or BreezecardNum duplication"



# Executions:
set_connection()
user_delete("123")
turnoff_connection()
