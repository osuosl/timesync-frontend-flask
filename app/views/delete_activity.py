from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
import pymesync
from app.util import is_logged_in, error_message, decrypter


@app.route('/activities/delete', methods=['GET', 'POST'])
def delete_activity():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.endpoint))

    user = session['user']

    if not user:
        return "There was an error.", 500

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=token)

    slug = request.args.get('slug')

    if not slug and request.method == 'GET':
        return 'UUID not found', 404

    if not user['site_admin']:
        return 'You cannot access this page.', 403

    form = forms.ConfirmDeleteForm(ts_object=slug)

    activity = ts.get_activities({"slug": slug})[0]

    if form.validate_on_submit():
        if 'ts_object' not in request.form:
            return 'UUID not found', 404

        slug = request.form['ts_object']
        response = ts.delete_activity(slug=slug)

        if not error_message(response):
            flash('Deletion successful')

        return redirect(url_for('view_activities'))

    if error_message(activity):
        activity = dict()

    return render_template('delete_activity.html', form=form,
                           activity=activity, is_logged_in=True,
                           is_admin=session['user']['site_admin'])
