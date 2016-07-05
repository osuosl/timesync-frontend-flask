from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message
import pymesync


@app.route('/projects/', methods=['GET', 'POST'])
def view_projects():
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])

    session_user = session['user']
    error_message(session_user)

    form = forms.FilterProjectsForm()

    query = {}

    if form.validate_on_submit():
        if request.form['name']:
            query['name'] = request.form['name']
        if request.form['slugs']:
            query['slugs'] = request.form['slugs'].split(',')
        if request.form['members']:
            query['members'] = request.form['members'].split(',')
        if request.form['managers']:
            query['managers'] = request.form['managers'].split(',')
        if request.form['spectators']:
            query['spectators'] = request.form['spectators'].split(',')

    elif request.method == 'POST' and not form.validate():
        flash("Invalid form input")

    projects = ts.get_projects(query_parameters=query)

    if error_message(projects):
        flash('Error')
        projects = []

    for project in projects:
        if 'users' in project:
            users = project['users']
            project['members'] = [user for user, permissions in
                                  users.iteritems() if permissions['member']]
            project['managers'] = [user for user, permissions in
                                   users.iteritems() if permissions['manager']]
            project['spectators'] = [user for user, permissions in
                                     users.iteritems() if
                                     permissions['spectator']]

    return render_template('view_projects.html', form=form, projects=projects,
                           user=session_user['username'],
                           admin=session_user['site_admin'])
