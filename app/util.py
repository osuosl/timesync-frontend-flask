from flask import session, flash
from app import app
from app.views.logout import logout
from datetime import datetime
import pymesync


def get_user(username):
    if not is_logged_in():
        print "Error: Not logged in"
        return {}

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])

    user = ts.get_users(username=username)[0]

    if 'error' in user or 'pymesync error' in user:
        print user
        return {}

    # If in testing mode and the username is admin, allow admin access
    if app.config['TESTING'] and user['username'] == 'admin':
        user['site_admin'] = True

    return user


def get_projects(username):
    if not is_logged_in():
        print "Error: Not logged in"
        return []

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])

    projects = ts.get_projects()

    if 'error' in projects:
        print projects['error']
        return []

    user_projects = []

    # Get each project the user has access to
    for project in projects:
        if 'users' in project and username in project['users']:
            user_projects.append(project)

    return user_projects


def is_logged_in():
    """Checks if the user is logged in. Also checks token expiration time,
        logging the user out if their token is expired."""

    if 'token' not in session:
        return False

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])

    expire = ts.token_expiration_time()

    if type(expire) is dict and ('error' in expire or
                                 'pymesync error' in expire):
        return False

    if datetime.now() > expire and not app.config['TESTING']:
        logout()
        return False

    return True


def error_message(obj):
    # obj is empty, there was an error
    if not obj:
        return True

    # Make sure obj is dict
    obj = obj if type(obj) is dict else obj[0]

    if 'error' in obj:
        flash("Error: " + obj["error"] + " - " + obj["text"])
        # There was an error
        return True
    elif 'pymesync error' in obj:
        flash("Error: " + obj["pymesync error"])
        # There was an error
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
