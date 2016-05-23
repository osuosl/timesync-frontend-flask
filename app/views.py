from flask import session, redirect, url_for, request, render_template, flash
from app import app
from datetime import datetime
import pymesync
import forms
import re


def is_logged_in():
    """Checks if the user is logged in. Also checks token expiration time,
        logging the user out if their token is expired."""

    if 'token' not in session:
        return False

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])

    expire = ts.token_expiration_time()

    if type(expire) is dict and ('error' in expire or
                                 'pymesync error' in expire):
        return False

    if datetime.now() > expire and not app.config['TESTING']:
        logout()
        return False

    return True


def get_user():
    if not is_logged_in():
        return {'error': "Not logged in."}

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])
    user = ts.get_users(username=session['username'])

    # If in testing mode and the username is admin, allow admin access
    if app.config['TESTING'] and session['username'] == 'admin':
        user[0]['site_admin'] = True

    return user


def to_readable_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    return '{}h{}m'.format(hours, minutes)


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
            session['username'] = username
            session['token'] = token['token']
            return form.redirect(url_for('index'))

    # Else if POST request (meaning form invalid), notify user
    elif request.method == 'POST':
        flash("Invalid submission.")
        status = 401

    return render_template('login.html', form=form), status


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('token', None)
    return redirect(url_for('index'))


@app.route('/times/create', methods=['GET', 'POST'])
def create_time():
    # Check if logged in first
    if not is_logged_in():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.url_rule))
        elif request.method == 'POST':
            return "Not logged in.", 401

    form = forms.CreateTimeForm()

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])

    projects = ts.get_projects()

    # TODO: Better error handling
    if 'error' in projects or 'pymesync error' in projects:
        return "There was an error.", 500

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
        if 'error' in res or 'pymesync error' in res:
            return "There was an error.", 500

        flash("Time successfully submitted.")
        return redirect(url_for('index'))

    # Flash any form errors
    for field, errors in form.errors.items():
        for error in errors:
            flash("%s %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

    # If not submitted (GET)

    return render_template('create_time.html', form=form)


@app.route('/times/edit', methods=['GET', 'POST'])
def edit_time():
    # Check if logged in first
    if not isLoggedIn():
        return redirect(url_for('login', next=request.url_rule))

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=session['token'])

    projects = ts.get_projects()

    # TODO: Better error handling
    if 'error' in projects or 'pymesync error' in projects:
        return "There was an error.", 500

    choices = []
    for project in projects:
        choices.append((project['name'], project['name']))

    uuid = request.args.get('time') if not ts.test else 'test'

    time = ts.get_times({'uuid': uuid})

    if ts.test:
        time = time[0]

    if 'error' in time or 'pymesync error' in time:
        return 'There was an error', 500

    if time['user'] != session['username']:
        return "Permission denied", 500

    time_data = {
        "duration": str(to_readable_time(time['duration'])),
        "user": str(session['username']),
        "project": str(time['project'][0]),
        "date_worked": datetime.strptime(time['date_worked'], "%Y-%m-%d"),
        "activities": '',
        "notes": '',
        "issue_uri": ''
    }

    if time['activities']:
        time_data['activities'] = ','.join(time['activities'])
    if time['notes']:
        time_data['notes'] = str(time['notes'])
    if time['issue_uri']:
        time_data['issue_uri'] = str(time['issue_uri'])

    form = forms.SubmitTimesForm(data=time_data)

    form.project.choices = choices

    # If the form has been submitted and validated we will update the time
    if form.validate_on_submit():
        req_form = request.form

        duration = req_form['duration']
        project = req_form['project']
        date_worked = req_form['date_worked']
        activities = req_form['activities'].split(',')
        notes = req_form['notes']
        issue_uri = req_form['issue_uri']

        time_update = dict()

        if duration != time_data['duration']:
            time_update['duration'] = duration
        if project != time_data['project']:
            time_update['project'] = project
        if date_worked != datetime.strftime(time_data['date_worked'],
                                            '%Y-%m-%d'):
            time_update['date_worked'] = date_worked
        if activities != time_data['activities'].split(','):
            time_update['activities'] = activities
        if notes != time_data['notes']:
            time_update['notes'] = notes
        if issue_uri != time_data['issue_uri']:
            time_update['issue_uri'] = issue_uri

        res = ts.update_time(uuid=uuid, time=time_update)

        if 'error' in res or 'pymesync error' in res:
            return 'There was an error', 500

        flash("Time successfully updated")
        return redirect(url_for('view_times'))

    # Flash any form errors
    for field, errors in form.errors.items():
        for error in errors:
            flash("%s %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

    return render_template('create_time.html', form=form)


@app.route('/times', methods=['GET', 'POST'])
def view_times():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=session['token'])

    # Form for filter parameters
    form = forms.FilterTimesForm()

    # Dictionary to store filter parameters
    query = dict()

    # If the form has been submitted and validated use the form's parameters
    if form.validate_on_submit():
        req_form = request.form

        user = req_form['user']
        projects = req_form['project']
        activities = req_form['activity']
        start = req_form['start']
        end = req_form['end']

        # Only using filter parameters that have been supplied
        if user:
            query['user'] = [user]
        if projects:
            query['project'] = [p.strip() for p in projects.split(',')]
        if activities:
            query['activity'] = [a.strip() for a in activities.split(',')]
        if start:
            query['start'] = [start]
        if end:
            query['end'] = [end]

    # If the form's parameters are not valid, tell the user
    elif request.method == 'POST' and not form.validate():
        flash("Invalid form input")

    times = ts.get_times(query_parameters=query)

    # Show any errors
    if 'error' in times or 'pymesync error' in times:
        flash("Error")
        flash(times)
        times = list()

    return render_template('view_times.html', form=form, times=times,
                           user=session['username'])


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
