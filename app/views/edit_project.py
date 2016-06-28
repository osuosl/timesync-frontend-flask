from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message
import pymesync
import re


@app.route('/projects/edit', methods=['GET', 'POST'])
def edit_project():
    if not is_logged_in():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.url_rule))
        elif request.method == 'POST':
            return "Not logged in.", 401

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])

    users = ts.get_users()
    error_message(users)

    usernames = []
    for user in users:
        usernames.append((user['username'], user['display_name']))

    slug = request.args.get('project')
    project = ts.get_projects({'slug': slug})[0]
    error_message(project)

    members = []
    managers = []
    spectators = []
    if 'users' in project:
        for user in project['users']:
            if project['users'][user]['member'] is True:
                members.append(user)
            if project['users'][user]['manager'] is True:
                managers.append(user)
            if project['users'][user]['spectator'] is True:
                spectators.append(user)

    project_data = {
        "members": members,
        "managers": managers,
        "spectators": spectators,
        "name": str(project['name']),
        "slugs": ','.join(project['slugs']),
        "uri": ''
    }

    if project['uri']:
        project_data['uri'] = str(project['uri'])

    form = forms.CreateProjectForm(data=project_data)

    # Enter choices
    form.members.choices = usernames
    form.managers.choices = usernames
    form.spectators.choices = usernames

    if form.validate_on_submit():
        project = {}
        permissions = {}

        for field in form:
            if field.data and field.name is not 'csrf_token':
                if field.name == 'slugs':
                    slugs = form.slugs.data
                    project['slugs'] = re.split('\s?,\s?', slugs)
                elif field.name == 'members':
                    for user in field.data:
                        if user in permissions:
                            permissions[user]['member'] = True
                        else:
                            permissions[user] = {}
                            permissions[user]['member'] = True
                elif field.name == 'managers':
                    for user in field.data:
                        if user in permissions:
                            permissions[user]['manager'] = True
                        else:
                            permissions[user] = {}
                            permissions[user]['manager'] = True
                elif field.name == 'spectators':
                    for user in field.data:
                        if user in permissions:
                            permissions[user]['spectator'] = True
                        else:
                            permissions[user] = {}
                            permissions[user]['spectator'] = True
                elif field.data != project_data[field.name]:
                    project[field.name] = field.data

        project['users'] = permissions

        res = ts.update_project(project=project, slug=slug)

        # TODO: Better error handling
        if 'error' in res:
            flash("Error: " + res['error'] + " - " + res['text'])
        elif 'pymesync error' in res:
            flash("Error: " + res['pymesync error'])

        flash("Project successfully submitted.")
        return redirect(url_for('view_projects'))

    for field, errors in form.errors.items():
        for error in errors:
            flash("%s %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

    return render_template('edit_project.html', form=form)
