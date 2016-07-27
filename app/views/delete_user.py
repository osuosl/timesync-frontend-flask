from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
import pymesync
from app.util import is_logged_in, error_message


@app.route('/users/delete', methods=['GET', 'POST'])
def delete_user():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    user = session['user']

    if not user:
        return "There was an error.", 500

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=session['token'])

    username = request.args.get('username')

    if not user['site_admin']:
        return 'You cannot access this page.', 403

    if not username:
        return 'Username not found', 404

    form = forms.ConfirmDeleteForm()

    # Need to be able to show the user's data
    delete_user = ts.get_users(username=username)[0]
    error_message(delete_user)

    if form.validate_on_submit():
        response = ts.delete_user(username=username)
        if not error_message(response):
            flash('Deletion successful')

        return redirect(url_for('view_users'))

    return render_template('delete_user.html', form=form,
                           delete_user=delete_user, user=user)