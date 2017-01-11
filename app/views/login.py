from flask import session, url_for, request, render_template, flash, redirect
from app import app, forms
from app.util import get_user, error_message, get_users, get_projects, \
                     get_activities, encrypter, is_logged_in
import pymesync


@app.route('/login/', methods=['GET', 'POST'])
def login():
    status = 200
    form = forms.LoginForm()

    # If POST request and form valid, login user
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        auth_type = form.auth_type.data

        # Login to TimeSync
        ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                               test=app.config['TESTING'])
        token = ts.authenticate(username=username,
                                password=password,
                                auth_type=auth_type)

        # If no error, proceed
        if not error_message(token):
            session['token'] = encrypter(token['token'])

            user = get_user(username)

            if not user:
                error_message(user)
                return 'There was an error.', 500

            all_projects = get_projects()
            projects = get_projects(username)
            activities = get_activities(username)
            users = get_users()

            user['projects'] = projects
            user['activities'] = activities

            session['projects'] = all_projects
            session['users'] = users
            session['user'] = user

            # Preserve query values from redirecting page
            redirect_args = dict(request.args)
            if 'next' in redirect_args:
                del redirect_args['next']

            if 'next' in request.args:
                next_url = url_for(request.args['next'], **redirect_args)
            else:
                next_url = url_for('index')

            return redirect(next_url)

    # Else if POST request (meaning form invalid), notify user
    elif request.method == 'POST':
        flash("Invalid submission.")
        status = 401

    logged_in = is_logged_in()

    return render_template('login.html', form=form,
                           is_logged_in=logged_in,
                           is_admin=session['user']['site_admin'] if logged_in
                           else False), status
