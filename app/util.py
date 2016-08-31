from flask import session, flash
from app import app
from app.views.logout import logout
from cgi import escape
from datetime import datetime
from Crypto.Cipher import AES
import pymesync


def get_user(username):
    if not is_logged_in():
        print "Error: Not logged in"
        return {}

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=token)

    user = ts.get_users(username=username)[0]

    if 'error' in user or 'pymesync error' in user:
        print user
        return {}

    # If in testing mode and the username is admin, allow admin access
    if app.config['TESTING'] and user['username'] == 'admin':
        user['site_admin'] = True

    return user


def get_users():
    if not is_logged_in():
        print "Error: Not logged in"
        return []

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=token)

    users = ts.get_users()

    if error_message(users):
        print users
        return []

    return users


def get_projects(username=None):
    if not is_logged_in():
        print "Error: Not logged in"
        return []

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=token)

    projects = ts.get_projects()

    if 'error' in projects:
        print projects['error']
        return []

    if not username:
        return projects

    user_projects = []

    # Get each project the user has access to
    for project in projects:
        if 'users' in project and username in project['users']:
            user_projects.append(project)

    return user_projects


def get_activities(username):
    if not is_logged_in():
        print "Error: Not logged in"
        return []

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=token)

    activities = ts.get_activities()

    if 'error' in activities:
        print activities['error']
        return []

    return activities


def is_logged_in():
    """Checks if the user is logged in. Also checks token expiration time,
        logging the user out if their token is expired."""

    if 'token' not in session:
        return False

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=token)

    expire = ts.token_expiration_time()

    if type(expire) is dict and ('error' in expire or
                                 'pymesync error' in expire):
        return False

    if datetime.now() > expire and not app.config['TESTING']:
        logout()
        return False

    return True


def format_error_message(err):
    if 'error' in err:
        error_type = err['error']
        error_text = err['text']

        if error_type == 'Bad Query Value':
            split_text = error_text.split(' ', 5)
            invalid_param = split_text[1]
            invalid_value = escape(split_text[5])

            msg = ('Error: Bad Query Value - Parameter <em>{}</em> contained '
                 + 'invalid value "<em>{}</em>"').format(invalid_param,
                                                         invalid_value)

    elif 'pymesync error' in err:
        msg = '{pymesync error}'.format(**err)
    else:
        msg = 'Unrecognized error'

    return msg


def error_message(obj):
    # obj is empty, no error
    if not obj:
        return False

    # Make sure obj is dict
    obj = obj if type(obj) is dict else obj[0]

    if 'error' in obj or 'pymesync error' in obj:
        flash(format_error_message(obj))
        return True

    # No error
    return False


def to_readable_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return '{}h{}m'.format(hours, minutes)


def project_user_permissions(form):
    users = form['members'].data + \
        form['managers'].data + \
        form['spectators'].data

    permissions = {}
    for user in users:
        user_permissions = {
            "member": user in form['members'].data,
            "manager": user in form['managers'].data,
            "spectator": user in form['spectators'].data
        }
        permissions[user] = user_permissions

    return permissions


# Padding for encryption
# Take a string (e becomes s inside the lambda). Take the block size minus the
# length of the string mod the block size (how many chars you need to pad the
# string out to the block size) and multiply by the ascii charcter
# representation of the number of chars you need to pad. Then add those char
# strings to the end of the original string, thereby padding it out to the
# block size with ascii char strings.
def pad(e):
    # Block size
    BS = 16
    return (lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS))(e)


# Unpadding for decryption
# Working from the inside out: Get the last character the string (e becomes s
# in the lambda). Get the ord() of that character - which from the last lambda
# should be the number of characters we padded the original string with. Then
# measure from the end of our string backwards the number of characters we
# added (which ord of the last character gave us). Get all the characters in
# the string up to that point. So if we added 10 chars, get all the chars in
# the string up to 10 from the end. Which leaves us with the original string.
def unpad(e):
    return (lambda s: s[:-ord(s[len(s)-1:])])(e)


def encrypter(e):
    encrypt = AES.new(app.config['ENCRYPTION_KEY'], AES.MODE_ECB)
    padded = pad(e)
    return encrypt.encrypt(padded)


def decrypter(e):
    decrypt = AES.new(app.config['ENCRYPTION_KEY'], AES.MODE_ECB)
    padded = decrypt.decrypt(e)
    return unpad(padded)
