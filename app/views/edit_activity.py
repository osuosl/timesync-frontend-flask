from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
import pymesync
from app.util import is_logged_in, get_user


@app.route('/activities/edit', methods=['GET', 'POST'])
def edit_activity():
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

    slug = request.args.get('slug')

    activity = ts.get_activities(query_parameters={"slug": slug})[0]

    if 'error' in activity or 'pymesync error' in activity:
        print activity
        return 'There was an error', 500

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

        if 'error' in res or 'pymesync error' in res:
            print res
            print activity_update
            return 'There was an error', 500

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

    return render_template('create_activity.html', form=form)
