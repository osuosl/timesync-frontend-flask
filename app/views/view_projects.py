from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, get_user
import pymesync


@app.route('/projects', methods=['GET'])
def view_projects():
    # Check if logged in first
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=session['token'])

    user = get_user()

    projects = ts.get_projects()

    if 'error' in projects[0] or 'pymesync error' in projects[0]:
        flash('Error')
        flash(projects)
        projects = list()

    return render_template('view_projects.html', projects=projects,
                           is_admin=user['site_admin'])
