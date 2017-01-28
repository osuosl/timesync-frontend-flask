from flask import session, flash
from app import app
from app.views.logout import logout
from cgi import escape
from datetime import datetime, timedelta
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


def get_activities():
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


def update_cached_projects():
    """Updates the projects in the session cache"""

    if not is_logged_in():
        return

    session["user"]["projects"] = get_projects(session["user"]["username"])
    session["projects"] = get_projects()


def update_cached_activities():
    """Updates the activities in the session cache"""

    if not is_logged_in():
        return

    session["user"]["activities"] = get_activities()


def update_cached_users(username=None):
    """Updates the users in the session cache"""

    if not is_logged_in():
        return

    # Update the current user
    if not username:
        username = session["user"]["username"]

    user = get_user(username)

    if "user" in session:
        user_projects = session["user"]["projects"]
        activities = session["user"]["activities"]

        user["projects"] = user_projects
        user["activities"] = activities

    session["user"] = user

    # Update the cache of all users
    session["users"] = get_users()


def build_cache(username=None):
    """Rebuilds the session cache of projects, activities, and users"""

    if not is_logged_in():
        return

    update_cached_users(username)
    update_cached_activities()
    update_cached_projects()

    # Add expiration time before next cache update
    session["next_update"] = datetime.now() + \
                             timedelta(minutes=app.config["CACHE_EXP"])


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
        error_type = err.get('error')
        error_text = err.get('text')

        if error_type:
            error_type = escape(error_type)

        if error_text:
            error_text = escape(error_text)

        if error_type == 'Object not found':
            split_text = error_text.split(' ', 1)
            nonexistent_obj = split_text[1]

            msg = ('Error: Object not found - ' +
                   'Nonexistent <em>{}</em>').format(nonexistent_obj)
        elif error_type == 'Invalid foreign key':
            split_text = error_text.split(' ')
            object_type = split_text[1]
            foreign_key = split_text[7]

            msg = ('Error: The <em>{}</em> does not contain a valid ' +
                   '<em>{}</em> reference').format(object_type, foreign_key)
        elif error_type == 'Invalid identifier':
            split_text = error_text.split(' ', 4)
            identifier = split_text[1]
            received = split_text[4]

            msg = ('Error: Invalid identifier - Expected <em>{}</em> but ' +
                   'received <em>{}</em>').format(identifier, received)
        elif 'Slug already exist' in error_type:  # Optional 's' at end
            slugs = ', '.join(err['values'])

            if len(err['values']) > 1:
                format_msg = 'Slugs <em>{}</em> already exist on another ' \
                           + 'object'
            else:
                format_msg = 'Slug <em>{}</em> already exists on another ' \
                           + 'object'

            msg = format_msg.format(slugs)
        elif error_type == 'Authorization failure':
            split_text = error_text.split(' ', 5)
            username = split_text[0]
            action = split_text[5]

            msg = ('Error: Authorization failure - <em>{}</em> is not ' +
                   'authorized to <em>{}</em>').format(username, action)
        elif error_type == 'Method Not Allowed':
            split_text = error_text.split(' ')
            obj_type = split_text[8]

            msg = ('Error: Method Not Allowed - The method specified is not ' +
                   'allowed for the <em>{}</em> identified').format(obj_type)
        elif error_type == 'Bad Query Value':
            split_text = error_text.split(' ', 5)
            invalid_param = split_text[1]
            invalid_value = split_text[5]

            msg = ('Error: Bad Query Value - Parameter <em>{}</em> ' +
                   'contains invalid value <em>{}</em>').format(invalid_param,
                                                                invalid_value)
        elif error_type == 'Username already exists':
            username = err['values'][0]

            msg = ('Error: Username already exists - Username <em>{}</em> ' +
                   'already exists').format(username)
        elif not error_text:
            msg = 'Error: {}'.format(error_type)
        else:
            msg = 'Error: {} - {}'.format(error_type, error_text)

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
    encrypt = AES.new(app.config['ENCRYPTION_KEY'], AES.MODE_CBC,
                      app.config['INITIALIZATION_VECTOR'])
    padded = pad(e)
    return encrypt.encrypt(padded)


def decrypter(e):
    decrypt = AES.new(app.config['ENCRYPTION_KEY'], AES.MODE_CBC,
                      app.config['INITIALIZATION_VECTOR'])
    padded = decrypt.decrypt(e)
    return unpad(padded)
