from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message
import pymesync


@app.route('/times', methods=['GET', 'POST'])
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

    # If the form's parameters are not valid, tell the user
    elif request.method == 'POST' and not form.validate():
        flash("Invalid form input")

    times = ts.get_times(query_parameters=query)

    # Show any errors
    error_message(times)

    return render_template('view_times.html', form=form, times=times,
                           user=user['username'], admin=user['site_admin'])
