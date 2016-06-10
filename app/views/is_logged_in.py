from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from datetime import datetime
import pymesync
import re

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
