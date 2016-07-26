from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from datetime import datetime
import pymesync
from app.util import is_logged_in, to_readable_time, error_message


@app.route('/times/edit/', methods=['GET', 'POST'])
def edit_time():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=session['token'])

    user = session['user']

    if not user:
        return 'There was an error.', 500

    projects = ts.get_projects()
    uuid = request.args.get('time')
    times = ts.get_times({'uuid': uuid})

    if not error_message(projects) and not error_message(times):
        choices = []
        for project in projects:
            choices.append((project['slugs'][0], project['name']))

        time = times[0]

        if time['user'] != user['username'] and not user['site_admin']:
            return "Permission denied", 500

        time_data = {
            "duration": str(to_readable_time(time['duration'])),
            "user": str(time['user']),
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

        form = forms.CreateTimeForm(data=time_data)

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

            if not error_message(res):
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
