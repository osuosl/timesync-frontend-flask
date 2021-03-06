from flask import session, redirect, url_for, request, render_template
from app import app
from app.util import is_logged_in, error_message, decrypter
import pymesync


@app.route('/times/user/', defaults={'username': ''})
@app.route('/times/user/<username>')
def view_user_times(username):
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.endpoint))

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=token)

    user = session['user']

    if not user:
        return 'There was an error', 500

    times = ts.get_times(query_parameters={'user': [username]})

    if error_message(times):
        print times
        times = []

    return render_template('view_user_times.html', times=times, user=user,
                           is_logged_in=True, is_admin=user['site_admin'])
