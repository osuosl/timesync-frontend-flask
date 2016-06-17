from flask import session, redirect, url_for, request, render_template, flash
from app import app
from app.util import is_logged_in, get_user
import pymesync


@app.route('/users', methods=['GET'])
def view_users():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=session['token'])

    users = ts.get_users()

    if 'error' in users[0] or 'pymesync error' in users[0]:
        flash('Error')
        flash(users)
        users = list()

    user = get_user()

    return render_template('view_users.html', users=users,
                           is_admin=user['site_admin'])
