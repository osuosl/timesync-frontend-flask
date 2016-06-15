from flask import session, redirect, url_for, request, render_template
from app import app
import pymesync
from app.util import is_logged_in, get_user


@app.route('/activities', methods=['GET'])
def view_activities():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    is_admin = False
    user = get_user()

    if 'error' in user or 'pymesync error' in user:
        print user
        return "There was an error.", 500

    is_admin = user['site_admin']

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=session['token'])

    activities = ts.get_activities()

    if 'error' in activities or 'pymesync error' in activities:
        print activities
        return "There was an error.", 500

    return render_template('view_activities.html', activities=activities,
                           is_admin=is_admin)
