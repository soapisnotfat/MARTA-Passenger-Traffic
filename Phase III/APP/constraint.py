import re

'''
Globals:
'''
email_format = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
username_format = "(^[a-zA-Z0-9_.-]{8,50}$)"
username_format_test = "(^[a-zA-Z0-9_.-]{,5}$)"
password_format = "(^[a-zA-Z0-9_.-]{8,50}$)"
password_format_test = "(^[a-zA-Z0-9_.-]{4}$)"


# check email format
#
# returns
#     1 - email matches format
#     0 - email doesn't match format
def constraint_email_format(email):
    email_regex = re.compile(email_format)
    if email_regex.match(email) is None:
        return 0
    else:
        return 1

# check username format
#
# returns
#     1 - username matches format
#     0 - usernmae doesn't match format
def constraint_username_format(username):
    username_regex = re.compile(username_format)
    if username_regex.match(username) is None:
        return 0
    else:
        return 1

# check password format
#
# returns
#     1 - password matches format
#     0 - password doesn't match format
def constraint_password_format(password):
    password_regex = re.compile(password_format)
    if password_regex.match(password) is None:
        return 0
    else:
        return 1
