from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.views.is_logged_in import is_logged_in
import pymesync
import re


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
        return projects['error'] + " " + projects['text'], 500

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
            return res['error'] + " " + res['text'], 500

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
