from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.views.is_logged_in import is_logged_in
from app.views.get_user import get_user
from datetime import datetime
import pymesync
import re

@app.route('/admin')
def admin():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    # Check if the user is an admin and deny access if not
    is_admin = False
    user = get_user()

    if 'error' in user or 'pymesync error' in user:
        print user
        return "There was an error.", 500

    if type(user) is dict:
        is_admin = user['site_admin']
    elif type(user) is list:
        is_admin = user[0]['site_admin']

    if not is_admin:
        return "You cannot access this page.", 401

    return render_template('admin.html')
