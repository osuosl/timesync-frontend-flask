from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
import pymesync
from app.util import is_logged_in, error_message, decrypter


@app.route('/times/delete/<uuid>', methods=['GET', 'POST'])
def delete_time(uuid):
    print(uuid)
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=token)

    time = ts.get_times({"uuid": uuid})[0]

    user = session['user']

    if time['user'] != user['username'] and not user['site_admin']:
        return 'Permission Denied', 500

    # Form to confirm deletion
    form = forms.ConfirmDeleteForm(uuid=uuid)

    if form.validate_on_submit():
        response = ts.delete_time(uuid=uuid)

        if not error_message(response):
            flash('Deletion successful')

        return redirect(url_for('view_times'))

    if error_message(time):
        time = dict()

    return render_template('delete_time.html', form=form, time=time)
