from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message, decrypter, project_members, \
                     project_managers, project_spectators
import pymesync


@app.route('/projects/', methods=['GET', 'POST'])
def view_projects():
    if not is_logged_in():
        return redirect(url_for('login', next=request.endpoint))

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=token)

    session_user = session['user']
    error_message(session_user)

    form = forms.FilterProjectsForm()

    query = {}

    if form.validate_on_submit():
        for field in form:
            if field.data and field.name is not 'csrf_token':
                query[field.name] = field.data
    elif request.method == 'POST' and not form.validate():
        flash("Invalid form input")

    if 'slug' in query and 'include_deleted' in query:
        flash('Invalid query: Cannot use "Slug" and "Include Deleted" at the \
               same time')
        query = {}

    projects = ts.get_projects(query_parameters=query)

    if error_message(projects):
        flash('Error')
        projects = []

    for project in projects:
        if 'users' in project:
            project['members'] = project_members(project)
            project['managers'] = project_managers(project)
            project['spectators'] = project_spectators(project)

    return render_template('view_projects.html', form=form, projects=projects,
                           user=session_user, is_logged_in=True,
                           is_admin=session_user['site_admin'])
