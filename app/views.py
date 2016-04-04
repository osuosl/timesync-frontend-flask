from flask import session, redirect, url_for, render_template
from app import app
from datetime import timedelta
import pymesync
import forms


# Expires users after 30 minutes OF UNACTIVITY
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@app.route('/')
def index():
    return 'Welcome to timesync-frontend.'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()

    # TODO: Flash message on invalid submission
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Login to TimeSync
        ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'])
        token = ts.authenticate(username=username,
                                password=password,
                                auth_type="password")

        # TODO: Better error handling
        if 'error' in token or 'pymesync error' in token:
            print token
            return 'There was an error.', 500

        session['username'] = username
        session['token'] = token['token']
        return redirect(url_for('index'))

    return render_template('login.html', form=form)
