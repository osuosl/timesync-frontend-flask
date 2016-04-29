from flask import session, redirect, url_for, request, render_template, flash
from app import app, redis
from datetime import timedelta
import pymesync
import forms
import re


def token_name(user):
    return '{}:token'.format(user)


def is_logged_in():
    """Checks if the user is logged in. Also checks token expiration time,
       logging the user out if their token is expired."""

    if 'user' not in session:
        return False

    # If not in redis database, key has expired
    if not redis.exists(token_name(session['user'])):
        logout()  # Remove 'user' from session
        return False

    return True


# Expires users after 30 minutes OF UNACTIVITY
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)


@app.route('/')
def index():
    return "Welcome to timesync-frontend."


@app.route('/login', methods=['GET', 'POST'])
def login():
    status = 200
    form = forms.LoginForm()

    # If POST request and form valid, login user
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Login to TimeSync
        ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                               test=app.config['TESTING'])
        token = ts.authenticate(username=username,
                                password=password,
                                auth_type='password')

        # If regular error, tell user error
        if 'error' in token:
            flash(token['text'])
            status = token['status']
        # If pymesync error, tell user vague error
        elif 'pymesync error' in token:
            print token
            return "There was an error.", 500
        # Else success, redirect to index page
        else:
            # Add a key to the redis database under the user's name and
            # set it to the token, then set the expiry time
            redis.set(token_name(username), token['token'])
            redis.expireat(token_name(username), ts.token_expiration_time())

            session['user'] = username

            return form.redirect(url_for('index'))

    # Else if POST request (meaning form invalid), notify user
    elif request.method == 'POST':
        flash("Invalid submission.")
        status = 401

    return render_template('login.html', form=form), status


@app.route('/logout')
def logout():
    # If currently logged in, remove the user's token from the database
    if 'user' in session:
        redis.delete(token_name(session['user']))

        session.pop('user', None)

    return redirect(url_for('index'))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    # Check if logged in first
    if not is_logged_in():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.url_rule))
        elif request.method == 'POST':
            return "Not logged in.", 401

    form = forms.SubmitTimesForm()

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=redis.get(token_name(session['user'])))

    projects = ts.get_projects()

    # Load the projects into a list of tuples
    choices = []
    for project in projects:
        choices.append((project['name'], project['name']))
    form.project.choices = choices

    # If form submitted (POST)
    if form.validate_on_submit():
        user = form.user.data
        project_name = form.project.data
        duration = form.duration.data
        date_worked = form.date_worked.data

        # Load optional fields, if they aren't blank
        activities = form.activities.data
        notes = form.notes.data
        issue_uri = form.issue_uri.data

        # With project name, get slug
        for project in projects:
            if project['name'] == project_name:
                project_name = project['slugs'][0]

        # Try to convert str to int, else just leave as str
        try:
            duration = int(duration)
        except:
            pass

        time = {
            "duration": duration,
            "user": user,
            "project": project_name,
            "date_worked": date_worked.strftime('%Y-%m-%d')
        }

        # If optional fields are not empty, add to time
        if activities:
            # Create list from comma delimited string
            time['activities'] = re.split('\s?,\s?', activities)
        if notes:
            time['notes'] = notes
        if issue_uri:
            time['issue_uri'] = issue_uri

        res = ts.create_time(time=time)

        # TODO: Better error handling
        if 'error' in res:
            return "There was an error.", 500

        flash("Time successfully submitted.")
        return redirect(url_for('submit'))

    # Flash any form errors
    for field, errors in form.errors.items():
        for error in errors:
            flash("%s %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

    # If not submitted (GET)

    return render_template('submit.html', form=form)
