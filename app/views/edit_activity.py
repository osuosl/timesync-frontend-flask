from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
import pymesync
from app.util import is_logged_in, error_message, decrypter, \
                     update_cached_activities


@app.route('/activities/edit/', methods=['GET', 'POST'])
def edit_activity():
    # Check if logged in first
    if not is_logged_in():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.endpoint,
                                    **request.args))
        elif request.method == 'POST':
            return "Not logged in.", 401

    # Check if the user is an admin and deny access if not
    is_admin = False
    user = session['user']

    if not user:
        return "There was an error.", 500

    is_admin = user['site_admin']

    if not is_admin:
        return "You cannot access this page.", 401

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=token)

    form = forms.CreateActivityForm()

    slug = request.args.get('slug')

    activities = ts.get_activities(query_parameters={"slug": slug})

    if not error_message(activities):
        activity = activities[0]

        if form.validate_on_submit():
            req_form = request.form

            # To preserve the old slug so we can call update_activity()
            old_slug = slug

            name = req_form['name']
            slug = req_form['slug']

            activity_update = dict()

            if name != activity['name']:
                activity_update['name'] = name
            if not ts.test and slug != activity['slug']:
                activity_update['slug'] = slug

            res = ts.update_activity(activity=activity_update, slug=old_slug)

            error_message(res)

            update_cached_activities()

            return redirect(url_for('view_activities'))

        # If GET
        form.name.data = activity['name']
        if ts.test:
            form.slug.data = activity['slug'][0]
        else:
            form.slug.data = activity['slug']

    for field, errors in form.errors.items():
        for error in errors:
            flash("%s %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

    return render_template('create_activity.html', form=form,
                           is_logged_in=True,
                           is_admin=session['user']['site_admin'])
