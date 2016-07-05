from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from app.util import is_logged_in, error_message, project_user_permissions
import pymesync


@app.route('/projects/create/', methods=['GET', 'POST'])
def create_project():
    if not is_logged_in():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.url_rule))
        elif request.method == 'POST':
            return "Not logged in.", 401

    form = forms.CreateProjectForm()

    ts = pymesync.TimeSync(baseurl=app.config['TIMESYNC_URL'],
                           test=app.config['TESTING'],
                           token=session['token'])

    users = ts.get_users()
    error_message(users)

    usernames = []
    for user in users:
        usernames.append((user['username'], user['display_name']))

    # Fill the multi-select boxes with usernames
    # In order to be able to select users for each permission, you must have a
    # list of users
    form.members.choices = usernames
    form.managers.choices = usernames
    form.spectators.choices = usernames

    if form.validate_on_submit():
        project = {}

        for field in form:
            exclude = ['csrf_token', 'members', 'managers', 'spectators']
            if field.data and field.name not in exclude:
                if field.name == 'slugs':
                    project['slugs'] = form.slugs.data.split(',')
                else:
                    project[field.name] = field.data

        project['users'] = project_user_permissions(form)

        res = ts.create_project(project=project)
        if not error_message(res):
            flash("Project successfully submitted.")

        return redirect(url_for('create_project'))

        # Flash any form errors
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} {1}".format(getattr(form, field).label.text, error),
                  'error')

    return render_template('create_project.html', form=form,
                           usernames=usernames)
