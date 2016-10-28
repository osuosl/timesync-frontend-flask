from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message, project_user_permissions, \
                     decrypter
import pymesync


@app.route('/projects/edit/', methods=['GET', 'POST'])
def edit_project():
    if not is_logged_in():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.url_rule))
        elif request.method == 'POST':
            return "Not logged in.", 401

    token = decrypter(session['token'])

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=token)

    users = ts.get_users()
    error_message(users)

    usernames = []
    for user in users:
        usernames.append((user['username'], user['display_name']))

    slug = request.args.get('project')
    project = ts.get_projects({'slug': slug})[0]
    error_message(project)

    user = session['user']
    if 'users' in project:
        if not user['username'] in project['users'] and not user['site_admin']:
            return "Permission denied", 403
    elif not user['site_admin']:
        return "Permission denied", 403

    if 'default_activity' in project:
        default_activity = str(project['default_activity'])
    else:
        default_activity = ''

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

    if 'name' in project:
        name = str(project['name'])
    else:
        name = ''
    if 'slugs' in project:
        slugs = ','.join(project['slugs'])
    else:
        slugs = ''

    project_data = {
        "members": members,
        "managers": managers,
        "spectators": spectators,
        "default_activity": default_activity,
        "name": name,
        "slugs": slugs,
        "uri": ''
    }

    if 'uri' in project:
        project_data['uri'] = str(project['uri'])

    form = forms.CreateProjectForm(data=project_data)

    form.default_activity.choices = [('', '')]
    form.default_activity.choices += [(a['slug'], a['name'])
                                      for a in session['user']['activities']]

    # Enter choices
    form.members.choices = usernames
    form.managers.choices = usernames
    form.spectators.choices = usernames

    if form.validate_on_submit():
        project = {}

        for field in form:
            # These are not project fields, don't take data from them here
            exclude = ['csrf_token', 'members', 'managers', 'spectators']
            if field.data and field.name not in exclude:
                if field.name == 'slugs':
                    slugs = form.slugs.data
                    project['slugs'] = slugs.split(',')
                elif field.data != project_data[field.name]:
                    project[field.name] = field.data

        project['users'] = project_user_permissions(form)

        res = ts.update_project(project=project, slug=slug)

        if not error_message(res):
            flash("Project successfully submitted.")

        return redirect(url_for('view_projects'))

    for field, errors in form.errors.items():
        for error in errors:
            flash("%s %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

    return render_template('edit_project.html', form=form)
