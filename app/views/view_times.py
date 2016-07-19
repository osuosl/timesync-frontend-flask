from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message
import pymesync


@app.route('/times/', methods=['GET', 'POST'])
def view_times():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=session['token'])

    user = session['user']

    if not user:
        return 'There was an error.', 500

    # Form for filter parameters
    form = forms.FilterTimesForm()

    # Dictionary to store filter parameters
    query = dict()

    # List of times
    times = list()

    # Dictionary to store summary information
    summary = dict()

    # If the form has been submitted and validated use the form's parameters
    if form.validate_on_submit():
        req_form = request.form

        username = req_form['user']
        projects = req_form['project']
        activities = req_form['activity']
        start = req_form['start']
        end = req_form['end']

        # Only using filter parameters that have been supplied
        if username:
            query['user'] = [u.strip() for u in username.split(',')]
        if projects:
            query['project'] = [p.strip() for p in projects.split(',')]
        if activities:
            query['activity'] = [a.strip() for a in activities.split(',')]
        if start:
            query['start'] = [start]
        if end:
            query['end'] = [end]

        times = ts.get_times(query_parameters=query)
#        print "PRINTING TIMES:"
#        print times
#        print "DONE PRINTING TIMES."
        
        # Find "total_time": sum duration's seconds
        total_time = 0
        unique_users = set()
        unique_projects = set()
        unique_activities = list() # empty list
        for entry in times:
            total_time += entry['duration']
            unique_users.add(entry['user'])
            unique_projects.add(tuple(entry['project']))
            unique_activities += entry['activities'] # add activities list to big list of activities, repeats included 

        # add to summary dict
        summary['total_time'] = total_time
        summary['unique_users'] = len(unique_users) # number of unique users
        summary['users_list'] = list(unique_users) # list of unique users
        summary['unique_projects'] = len(unique_projects) # num unique projs
        summary['projects_list'] = list(unique_projects) # list of uniq projs
        summary['unique_activities'] = len(set(unique_activities)) # num uniq act
        summary['activities_list'] = list(set(unique_activities)) # list uniq act

#        print summary

        # Find unique_users

        # Show any errors
        if error_message(times):
            times = list()

    # If the form's parameters are not valid, tell the user
    elif request.method == 'POST' and not form.validate():
        flash("Invalid form input")

    return render_template('view_times.html', form=form, times=times,
                           summary=summary, user=user['username'],
                           is_admin=user['site_admin'])
