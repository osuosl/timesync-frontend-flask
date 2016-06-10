from flask import session
from app import app
from app.views.is_logged_in import is_logged_in
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
