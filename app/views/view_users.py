from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message, get_user, decrypter
import pymesync


@app.route('/users/', methods=['GET', 'POST'])
def view_users():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=token)

    user = get_user(session['user']['username'])
    error_message(user)

    # Form for filter parameters
    form = forms.FilterUsersForm()

    # Dictionary to store filter parameters
    query = {}

    # If the form has been submitted and validated use the form's parameters
    if form.validate_on_submit():
        # Only using filter parameters that have been supplied
        if request.form['username']:
            query['username'] = request.form['username']

    # If the form's parameters are not valid, tell the user
    elif request.method == 'POST' and not form.validate():
        flash("Invalid form input")

    if 'username' in query:
        users = ts.get_users(username=query['username'])
    else:
        users = ts.get_users()

    # Show any errors
    if error_message(users):
        users = []

    return render_template('view_users.html', form=form, users=users,
                           user=user['username'], admin=user['site_admin'])
