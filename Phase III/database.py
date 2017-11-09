# imports
import config
from datetime import datetime
import MySQLdb
import re
import traceback


# Global variables
_connected = False
_database = None
_cursor = None


# setups - ignore this section
def setupConnection():
    global _connected
    global _database
    global _cursor

    if not _connected:
        try:
            _database = MySQLdb.connect(host="https://academic-mysql.cc.gatech.edu/phpmyadmin",
                                        user="cs4400_Group_91",
                                        passwd="_OY4gwQs",
                                        db="MartaTraffic")

            # _database = MySQLdb.connect(host="localhost",
            #                             user="root",
            #                             passwd="root",
            #                             db="MartaTraffic")

            _cursor = _database.cursor()
            _connected = True
            if _connected:
                print("hello")
            else:
                print("oh no")

        except Exception as e:
            _connected = False
            traceback.print_exc()


def closeConnection():
    global _connected

    if _connected:
        _database.close()
        _connected = False



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
    query = "SELECT * FROM USER WHERE username = %s AND password = %s;"
    response = _cursor.execute(query, (username, password))

    # clear cursor
    _cursor.fetchall()

    if response == 0:
        return 0
    else:
        query = "SELECT Is_manager FROM USER WHERE Username = %s;"
        response = _cursor.execute(query, username)

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
def user_insert(username, password, isAdmin):
    query = "INSERT INTO USER(username, password, isAdmin) VALUES (%s, %s, %s);"
    try:
        response = _cursor.execute(query, (username, password, isAdmin))
        _database.commit()
    except Exception as e:
        # TODO: check the violation conditions
        if e[1][-2:] == 'Y\'':  # violates primary key constraint, username
            return "username duplication"
        else:  # don't get here
            return "user other exception"


# delete tuples from user
def user_delete(username):
    query = "DELETE FROM USER WHERE username = %s"
    try:
        response = _cursor.execute(query, username)
        _database.commit()
    except Exception:
        # handle the exceptions


# insert tuple to user
def passenger_insert(username, email):
    email_regex = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if not email_regex.match(email):
        return "email format not match"

    query = "INSERT INTO PASSENGER(username, email) VALUES (%s, %s);"
    try:
        response = _cursor.execute(query, (username, email))
        _database.commit()
    except Exception as e:
        if xxx:
            return "email duplication"
        #TODO: check email uniqueness






# Executions:
setupConnection()
closeConnection()