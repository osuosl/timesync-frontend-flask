from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
import pymesync
from app.util import is_logged_in, get_user


@app.route('/activities/create', methods=['GET', 'POST'])
def create_activity():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    # Check if the user is an admin and deny access if not
    is_admin = False
    user = get_user()

    if 'error' in user or 'pymesync error' in user:
        print user
        return "There was an error.", 500

    is_admin = user['site_admin']

    if not is_admin:
        return "You cannot access this page.", 401

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=session['token'])

    form = forms.CreateActivityForm()

    if form.validate_on_submit():
        req_form = request.form

        name = req_form['name']
        slug = req_form['slug']

        activity = {
            "name": name,
            "slug": slug
        }

        res = ts.create_activity(activity=activity)

        if 'error' in res or 'pymesync error' in res:
            return "There was an error", 500

        flash('Activity successfully created')
        return redirect(url_for('admin'))

    # If GET
    for field, errors in form.errors.items():
        for error in errors:
            flash("%s %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

    return render_template('create_activity.html', form=form)
