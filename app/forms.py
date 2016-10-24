from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, DateField, \
    BooleanField, HiddenField, SelectMultipleField
from wtforms.validators import DataRequired, Optional, URL


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    auth_type = SelectField('Authentication Type', validators=[DataRequired()],
                            choices=[('ldap', 'LDAP'),
                                     ('password', 'Password')])


class CreateTimeForm(Form):
    duration = StringField('Duration:', validators=[DataRequired()])
    project = SelectField('Project:', choices=[], validators=[DataRequired()])
    date_worked = DateField('Date Worked:', format='%Y-%m-%d',
                            description='yyyy-mm-dd',
                            validators=[DataRequired()])

    # Optional
    activities = SelectMultipleField('Activities:')
    notes = StringField('Notes:')
    issue_uri = StringField('Issue URI:',
                            description='E.g. http://www.github.com')


class FilterTimesForm(Form):
    # All optional
    users = SelectMultipleField('User:')
    projects = SelectMultipleField('Project Slugs:')
    activities = SelectMultipleField('Activity Slugs:')
    start = DateField('Start Date:', format="%Y-%m-%d",
                      description='yyyy-mm-dd', validators=[Optional()])
    end = DateField('End Date:', format="%Y-%m-%d",
                    description='yyyy-mm-dd', validators=[Optional()])


class CreateActivityForm(Form):
    name = StringField('Activity Name:', validators=[DataRequired()])
    slug = StringField('Activity Slug:', validators=[DataRequired()])


class CreateProjectForm(Form):
    uri = StringField('URI:', validators=[URL(), DataRequired()])
    name = StringField('Name:', validators=[DataRequired()])
    slugs = StringField('Slugs:', validators=[DataRequired()])
    default_activity = SelectField("Default Activity:")
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
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    display_name = StringField('Display Name:')
    email = StringField('Email:')
    site_admin = BooleanField('Site Admin')
    site_spectator = BooleanField('Site Spectator')
    site_manager = BooleanField('Site Manager')
    active = BooleanField('Active')


class FilterUsersForm(Form):
    username = StringField('Username:')
    metainfo = StringField('Meta-information:')


class ConfirmDeleteForm(Form):
    ts_object = HiddenField()
