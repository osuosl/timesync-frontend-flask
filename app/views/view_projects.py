from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, get_user, error_message
import pymesync
import re


@app.route('/projects', methods=['GET', 'POST'])
def view_projects():
    if not is_logged_in():
        return redirect(url_for('login', next=request.url_rule))

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])

    user = get_user(session['user']['username'])
    error_message(user)

    projects = ts.get_projects()
    error_message(projects)

    form = forms.FilterProjectsForm()

    query = {}

    if form.validate_on_submit():
        if request.form['name']:
            query['name'] = request.form['name']
        if request.form['slugs']:
            query['slugs'] = re.split('\s?,\s?', request.form['slugs'])
        if request.form['members']:
            query['members'] = re.split('\s?,\s?', request.form['members'])
        if request.form['managers']:
            query['managers'] = re.split('\s?,\s?', request.form['managers'])
        if request.form['spectators']:
            query['spectators'] = re.split('\s?,\s?',
                                           request.form['spectators'])

    elif request.method == 'POST' and not form.validate():
        flash("Invalid form input")

    projects = ts.get_projects(query_parameters=query)
    error_message(projects)

    if 'error' in projects or 'pymesync error' in projects:
        flash('Error')
        projects = []

    for project in projects:
        project['members'] = []
        project['managers'] = []
        project['spectators'] = []

        if 'users' in project:
            for username in project['users']:
                if project['users'][username]['member']:
                    project['members'].append(username)
                if project['users'][username]['manager']:
                    project['managers'].append(username)
                if project['users'][username]['spectator']:
                    project['spectators'].append(username)

    return render_template('view_projects.html', form=form, projects=projects,
                           user=user['username'], admin=user['site_admin'])
