from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
import pymesync
from app.util import is_logged_in, error_message, decrypter, project_members, \
                     project_managers, project_spectators


@app.route('/projects/delete', methods=['GET', 'POST'])
def delete_project():
    # Check if logged in first
    if not is_logged_in():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.endpoint,
                                    **request.args))
        elif request.method == 'POST':
            return "Not logged in.", 401

    user = session['user']
    username = user['username']

    if not user:
        return "There was an error.", 500

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'], token=token)

    slug = request.args.get('slug')
    form = forms.ConfirmDeleteForm(ts_object=slug)

    if request.method == 'POST':
        slug = form['ts_object']

    if not slug:
        return 'Project not found', 404

    project = ts.get_projects({'slug': slug})

    if not project:
        return 'Project not found', 404

    project = project[0]

    # Convert project user permissions into a more useful format
    if 'users' in project:
        project['members'] = project_members(project)
        project['managers'] = project_managers(project)
        project['spectators'] = project_spectators(project)
    else:
        project['members'] = []
        project['managers'] = []
        project['spectators'] = []

    if not user['site_admin'] and username not in project['managers']:
        return 'You cannot access this page.', 403

    if form.validate_on_submit():
        if 'ts_object' not in request.form:
            return 'Project slug not found', 404

        slug = request.form['ts_object']
        response = ts.delete_project(slug=slug)

        if not error_message(response):
            flash('Deletion successful')

        return redirect(url_for('view_projects'))

    return render_template('delete_project.html', form=form,
                           project=project, user=user,
                           is_logged_in=True)
