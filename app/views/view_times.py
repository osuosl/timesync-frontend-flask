from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message, decrypter
import pymesync


@app.route('/times/', methods=['GET', 'POST'])
def view_times():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=token)

    user = session['user']

    if not user:
        return 'There was an error.', 500

    # Form for filter parameters
    form = forms.FilterTimesForm()

    # Dictionary to store filter parameters
    query = {}

    # List of times
    times = []

    # Dictionary to store summary information
    summary = {}

    # Set up form choices
    form.users.choices = [(u['username'], u['username'])
                          for u in session['users']]
    form.projects.choices = [(p['slugs'][0], p['name'])
                             for p in session['user']['projects']]
    form.activities.choices = [(a['slug'], a['name'])
                               for a in session['user']['activities']]

    # If the form has been submitted and validated use the form's parameters
    if form.validate_on_submit():
        username = form.users.data
        projects = form.projects.data
        activities = form.activities.data
        start = form.start.data
        end = form.end.data

        # Only using filter parameters that have been supplied
        if username:
            query['user'] = username
        if projects:
            query['project'] = projects
        if activities:
            query['activity'] = activities
        if start:
            query['start'] = [start]
        if end:
            query['end'] = [end]

        times = ts.get_times(query_parameters=query)

        print(times)

        # Show any errors
        if error_message(times):
            times = []

        # Generate summary information
        if times:
            total_time = 0
            unique_users = set()
            unique_projects = set()
            unique_activities = []
            for entry in times:
                total_time += entry['duration']
                unique_users.add(entry['user'])
                unique_projects.add(entry['project'][0])
                unique_activities += entry['activities']

            summary['total_time'] = (total_time)
            summary['unique_users'] = len(unique_users)
            summary['users_list'] = list(unique_users)
            summary['unique_projects'] = len(unique_projects)
            summary['projects_list'] = list(unique_projects)
            summary['unique_activities'] = len(set(unique_activities))
            summary['activities_list'] = list(set(unique_activities))

    # If the form's parameters are not valid, tell the user
    elif request.method == 'POST' and not form.validate():
        flash('Invalid form input')

    # Lines 87 and 89 were causing the times to show up by default regardless
    # of whether the form had been submitted or not.

    # times = ts.get_times(query_parameters=query)

    # Show any errors
    # error_message(times)

    return render_template('view_times.html', form=form, times=times,
                           summary=summary, user=user['username'],
                           is_admin=user['site_admin'], is_logged_in=True)
