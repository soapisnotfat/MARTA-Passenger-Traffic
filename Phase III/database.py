import config
from datetime import datetime
import MySQLdb
import re
import traceback


_connected = False
_database = None
_cursor = None

# setupConnection() must be called before anything else for this to work
# closeConnection() should be called after finishing


def setupConnection():
    global _connected
    global _database
    global _cursor

    if not _connected:
        try:
            _database = MySQLdb.connect(host="localhost",
                                        user="root",
                                        passwd="root",
                                        db="MartaTraffic")
            _cursor = _database.cursor()
            _connected = True
        except Exception as e:
            _connected = False
            traceback.print_exc()


def closeConnection():
    global _connected

    if _connected:
        _database.close()
        _connected = False


'''
register function that inserts tuples to database

returns:
    return 0 for register successfully
    return 1 for email doesn't match format
    return 2 for username duplication
    return 3 for email duplication
    return 4 for all other exceptions
'''
def register(username, password, email, isAdmin):
    # check the validity of email format
    email_regex = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if not email_regex.match(email):
        return 1

    query_1 = "INSERT INTO USER(username, password, isAdmin)" \
            "VALUES (%s, %s, %s);"

    query_2 = "INSERT INTO PASSENGER(username, email)" \
              "VALUES (%s, %s);"

    try:
        response = _cursor.execute(query_1, (username, password, isAdmin))
        _database.commit()
        # TODO: finish two queries & change the exception catcher
        return 0

    except Exception as e:
        # TODO: check the violation conditions
        if e[1][-2:] == 'Y\'':  # violates primary key constraint, username
            return 2
        elif e[1][-2:] == 'l\'':  # violates email uniqueness constraint
            return 3
        else:  # don't get here
            return 4


'''
login function that check the login status

returns:
    return 0 for failed tries
    return 1 for administrator login
    return 2 for passenger login
'''
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




# Executions:
setupConnection()
closeConnection()
