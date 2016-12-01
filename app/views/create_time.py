from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message, decrypter
import pymesync
import json


@app.route('/times/create/', methods=['GET', 'POST'])
def create_time():
    # Check if logged in first
    if not is_logged_in():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.url_rule))
        elif request.method == 'POST':
            return "Not logged in.", 401

    form = forms.CreateTimeForm()

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=token)

    form.project.choices = [(p['slugs'][0], p['name'])
                             for p in session['user']['projects']]
    form.activities.choices = [(a['slug'], a['name'])
                               for a in session['user']['activities']]

    default_activities = {p['slugs'][0]: p['default_activity']
                          for p in session['user']['projects']
                          if p['default_activity']}

    # If form submitted (POST)
    if form.validate_on_submit():
        project = form.project.data
        duration = form.duration.data
        date_worked = form.date_worked.data

        # Load optional fields, if they aren't blank
        activities = form.activities.data
        notes = form.notes.data
        issue_uri = form.issue_uri.data

        # Try to convert str to int, else just leave as str
        if duration.isdigit():
            duration = int(duration)

        time = {
            "duration": duration,
            "user": session['user']['username'],
            "project": project,
            "date_worked": date_worked.strftime('%Y-%m-%d')
        }

        # If optional fields are not empty, add to time
        if activities:
            time['activities'] = activities
        if notes:
            time['notes'] = notes
        if issue_uri:
            time['issue_uri'] = issue_uri

        res = ts.create_time(time=time)

        if not error_message(res):
            flash("Time successfully submitted.")
            return redirect(url_for('create_time'))

    # Flash any form errors
    for field, errors in form.errors.items():
        for error in errors:
            flash("%s %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

    # If not submitted (GET)
    return render_template('create_time.html', form=form, is_logged_in=True,
                           default_activities=json.dumps(default_activities),
                           is_admin=session['user']['site_admin'])
