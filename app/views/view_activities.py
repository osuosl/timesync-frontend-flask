from flask import session, redirect, url_for, request, render_template
from app import app, forms
import pymesync
from app.util import is_logged_in, error_message, decrypter


@app.route('/activities/', methods=['GET', 'POST'])
def view_activities():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.endpoint))

    is_admin = False
    user = session['user']

    if not user:
        return "There was an error.", 500

    is_admin = user['site_admin']

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=token)

    form = forms.FilterActivitiesForm()
    query = {}

    if form.validate_on_submit():
        slug = form.slug.data
        include_deleted = form.include_deleted.data
        include_revisions = form.include_revisions.data

        if slug:
            query["slug"] = slug
        if include_deleted:
            query["include_deleted"] = include_deleted
        if include_revisions:
            query["include_revisions"] = include_revisions

    activities = ts.get_activities(query_parameters=query)

    error_message(activities)

    return render_template('view_activities.html', form=form,
                           activities=activities, user=user,
                           is_logged_in=True, is_admin=is_admin)
