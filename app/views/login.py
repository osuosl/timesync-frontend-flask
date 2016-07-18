from flask import session, url_for, request, render_template, flash, redirect
from app import app, forms
from app.util import get_user, error_message
import pymesync


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
        error_message(token)
        if 'error' in token:
            status = token['status']
        # Else success, redirect to index page
        else:
            print session
            session['token'] = token['token']

            user = get_user(username)

            if not user:
                return 'There was an error.', 500

            session['user'] = user

            return redirect(request.args.get('next') or url_for('index'))

    # Else if POST request (meaning form invalid), notify user
    elif request.method == 'POST':
        flash("Invalid submission.")
        status = 401

    return render_template('login.html', form=form), status
