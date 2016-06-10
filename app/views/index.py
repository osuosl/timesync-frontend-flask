from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.views.is_logged_in import is_logged_in
from app.views.get_user import get_user
from datetime import datetime
import pymesync
import re

@app.route('/')
def index():
    is_admin = False
    logged_in = is_logged_in()

    if logged_in:
        user = get_user()
        if 'error' in user or 'pymesync error' in user:
            print user
            return "There was an error.", 500

        if type(user) is dict:
            is_admin = user['site_admin']

    return render_template('index.html', is_logged_in=logged_in,
                           is_admin=is_admin)
