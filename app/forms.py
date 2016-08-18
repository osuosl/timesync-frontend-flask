from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, DateField, \
    BooleanField, HiddenField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, URL


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()],
                           render_kw={'placeholder': 'username'})
    password = PasswordField('password', validators=[DataRequired()],
                             render_kw={'placeholder': 'password'})


class CreateTimeForm(Form):
    user = StringField('User:', validators=[DataRequired()])
    duration = StringField('Duration:', validators=[DataRequired()])
    project = SelectField('Project:', validators=[DataRequired()])
    date_worked = DateField('Date Worked:', format='%Y-%m-%d',
                            description='yyyy-mm-dd',
                            validators=[DataRequired()])

    # Optional
    activities = StringField('Activities:', description='Comma separated')
    notes = StringField('Notes:')
    issue_uri = StringField('Issue URI:',
                            description='E.g. http://www.github.com')


class FilterTimesForm(Form):
    # All optional
    user = StringField('User:')
    project = StringField('Project Slugs:', description='Comma separated')
    activity = StringField('Activity Slugs:', description='Comma separated')
    start = DateField('Start Date:', format="%Y-%m-%d",
                      description='yyyy-mm-dd', validators=[Optional()])
    end = DateField('End Date:', format="%Y-%m-%d",
                    description='yyyy-mm-dd', validators=[Optional()])


class CreateActivityForm(Form):
    name = StringField('Activity Name:')
    slug = StringField('Activity Slug:')


class CreateProjectForm(Form):
    uri = StringField('URI:', validators=[URL()])
    name = StringField('Name:')
    slugs = StringField('Slugs:')
    members = SelectMultipleField('Members')
    managers = SelectMultipleField('Managers')
    spectators = SelectMultipleField('Spectators')


class FilterProjectsForm(Form):
    username = StringField('Username:')
    slug = StringField('Slug:')
    include_deleted = BooleanField('Include Deleted:')
    include_revisions = BooleanField('Include Revisions:')


class FilterActivitiesForm(Form):
    # Optional
    slug = StringField('Activity Slug:')


class CreateUserForm(Form):
    username = StringField('Username:')
    password = PasswordField('Password:')
    display_name = StringField('Display Name:')
    email = StringField('Email:')
    site_admin = BooleanField('Site Admin:')
    site_spectator = BooleanField('Site Spectator:')
    site_manager = BooleanField('Site Manager:')
    active = BooleanField('Active:')


class FilterUsersForm(Form):
    username = StringField('Username:')


class ConfirmDeleteForm(Form):
    ts_object = HiddenField()
