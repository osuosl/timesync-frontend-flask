from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message
import pymesync


@app.route('/users/create/', methods=['GET', 'POST'])
def create_user():
    # Check if logged in first
    if not is_logged_in():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.url_rule))
        elif request.method == 'POST':
            return "Not logged in.", 401

    form = forms.CreateUserForm()

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])

    # If form submitted (POST)
    if form.validate_on_submit():
        user = {}

        for field in form:
            if field.data and field.name is not 'csrf_token':
                user[field.name] = field.data

        res = ts.create_user(user=user)

        error_message(res)

        flash("Time successfully submitted.")
        return redirect(url_for('create_user'))

    # Flash any form errors
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} {1}".format(getattr(form, field).label.text, error),
                  'error')

    # If not submitted (GET)
    return render_template('create_user.html', form=form)
