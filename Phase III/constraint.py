import re

'''
Globals:
'''
email_format = "(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
username_format = "(^[a-zA-Z]{,50})"
password_format = "(^[a-zA-Z]{,50})"


# check email format
#
# returns
#     1 - email matches format
#     2 - email doesn't match format
def constraint_email_format(email):
    email_regex = re.compile(email_format)
    return email_regex.match(email)

# check username format
#
# returns
#     1 - username matches format
#     2 - usernmae doesn't match format
def constraint_username_format(username):
    username_regex = re.compile(username_format)
    return username_regex.match(username)

# check password format
#
# returns
#     1 - password matches format
#     2 - password doesn't match format
def constraint_password_format(password):
    password_regex = re.compile(password_format)
    return password_regex.match(password)
