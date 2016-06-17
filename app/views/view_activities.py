from flask import session, redirect, url_for, request, render_template
from app import app
import pymesync
from app.util import is_logged_in, error_message


@app.route('/activities', methods=['GET'])
def view_activities():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    is_admin = False
    user = session['user']

    if not user:
        return "There was an error.", 500

    is_admin = user['site_admin']

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=session['token'])

    activities = ts.get_activities()

    error_message(activities)

    return render_template('view_activities.html', activities=activities,
                           is_admin=is_admin)
