from flask import redirect, url_for, request, render_template, session
from app import app
from app.util import is_logged_in, error_message


@app.route('/admin')
def admin():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    # Check if the user is an admin and deny access if not
    is_admin = False
    user = session['user']

    if not user:
        return "There was an error.", 500

    is_admin = user['site_admin']

    if not is_admin:
        return "You cannot access this page.", 401

    return render_template('admin.html')
