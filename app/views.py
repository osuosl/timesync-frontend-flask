from flask import session, redirect, url_for, request, render_template, flash
from app import app
from datetime import datetime
import pymesync
import forms
import re


def isLoggedIn():
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


def getUser():
    if not isLoggedIn():
        return {'error': "Not logged in."}

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])
    user = ts.get_users(username=session['username'])

    if (type(user) is list and session['username'] == 'admin' and
            app.config['TESTING']):

        user[0]['site_admin'] = True

    return user


@app.route('/')
def index():
    isAdmin = False
    loggedIn = isLoggedIn()

    if loggedIn:
        user = getUser()
        if 'error' in user or 'pymesync error' in user:
            print user
            return "There was an error.", 500

        if type(user) is dict:
            isAdmin = user['site_admin']

    return render_template('index.html', isLoggedIn=loggedIn,
                           isAdmin=isAdmin)


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


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    # Check if logged in first
    if not isLoggedIn():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.url_rule))
        elif request.method == 'POST':
            return "Not logged in.", 401

    form = forms.SubmitTimesForm()

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


@app.route('/report', methods=['GET', 'POST'])
def report():
    # Check if logged in first
    if not isLoggedIn():
        return redirect(url_for('login', next=request.url_rule))

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=session['token'])

    # Form for filter parameters
    form = forms.GenerateReportForm()

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

    return render_template('report.html', form=form, times=times)


@app.route('/admin')
def admin():
    # Check if logged in first
    if not isLoggedIn():
        return redirect(url_for('login', next=request.url_rule))

    # Check if the user is an admin and deny access if not
    isAdmin = False
    user = getUser()

    if 'error' in user or 'pymesync error' in user:
        print user
        return "There was an error.", 500

    if type(user) is dict:
        isAdmin = user['site_admin']
    elif type(user) is list:
        isAdmin = user[0]['site_admin']

    if not isAdmin:
        return "You cannot access this page.", 401

    return render_template('admin.html')
