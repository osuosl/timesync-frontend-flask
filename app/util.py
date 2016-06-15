from flask import session, flash
from app import app
from app.views.logout import logout
from datetime import datetime
import pymesync


def get_user():
    if not is_logged_in():
        return {'error': "Not logged in."}

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])
    user = ts.get_users(username=session['username'])

    # If in testing mode and the username is admin, allow admin access
    if app.config['TESTING'] and session['username'] == 'admin':
        user[0]['site_admin'] = True

    return user


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


def error_message(array):
    if 'error' in array:
        flash("Error: " + array["error"] + " - " + array["text"])
        # There was an error
        return True
    elif 'pymesync error' in array:
        flash("Error: " + array["pymesync error"] + " - " + array["text"])
        # There was an error
        return True

    # No error
    return False
