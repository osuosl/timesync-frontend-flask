from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message
import pymesync


@app.route('/users/edit/', methods=['GET', 'POST'])
def edit_user():
    # Check if logged in first
    if not is_logged_in():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.url_rule))
        elif request.method == 'POST':
            return "Not logged in.", 401

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])

    username = request.args.get('username')
    user = ts.get_users(username=username)[0]

    error_message(user)

    user_data = {
        'username': user['username'],
        'display_name': user['display_name'],
        'email': user['email'],
        'site_admin': user['site_admin'],
        'site_spectator': user['site_spectator'],
        'site_manager': user['site_manager'],
        'active': user['active']
    }

    form = forms.CreateUserForm(data=user_data)

    # If form submitted (POST)
    if form.validate_on_submit():
        user = {}
        for field in form:
            if field.data and field.name is not "csrf_token":
                if field.name is not 'password':
                    if field.data != user_data[field.name]:
                        user[field.name] = field.data
                else:
                    user[field.name] = field.data

        res = ts.update_user(user=user, username=form.username.data)

        error_message(res)

        flash("User successfully submitted.")
        return redirect(url_for('view_users'))

    # Flash any form errors
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} {1}".format(getattr(form, field).label.text, error),
                  'error')

    # If not submitted (GET)
    return render_template('edit_user.html', form=form)
