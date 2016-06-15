from flask import redirect, url_for, request, render_template
from app import app
from app.util import get_user, is_logged_in


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
