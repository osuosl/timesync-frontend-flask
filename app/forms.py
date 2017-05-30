from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField, DateField, \
    BooleanField, HiddenField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Optional, URL


class SelectWithDisable(object):
    """
    Renders a select field.

    If `multiple` is True, then the `size` property should be specified on
    rendering to make the field useful.

    The field must provide an `iter_choices()` method which the widget will
    call on rendering; this method must yield tuples of
    `(value, label, selected, disabled)`.
    """
    def __init__(self, multiple=False):
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)

        # Set 'selected' and 'disabled' to False for all fields except default
        for i, choice in enumerate(field.choices):
            field.choices[i] = choice + (False, False,)

        default_text = 'Choose option(s)' if self.multiple else 'Choose option'
        default = ('', default_text, True, True)
        field.choices.insert(0, default)

        if self.multiple:
            kwargs['multiple'] = 'multiple'
            kwargs['size'] = len(field.choices) \
                if len(field.choices) < 15 else 15

        html = [u'<select %s>' % widgets.html_params(
            name=field.name, **kwargs
        )]

        for val, label, selected, disabled in field.iter_choices():
            if field.data:
                if val == field.data or val in field.data:
                    selected = True

            html.append(self.render_option(val, label, selected, disabled))

        html.append(u'</select>')
        return widgets.HTMLString(u''.join(html))

    @classmethod
    def render_option(cls, value, label, selected, disabled):
        options = {'value': value}
        if selected:
            options['selected'] = u'selected'
        if disabled:
            options['disabled'] = u'disabled'
        return widgets.HTMLString(u'<option %s>%s</option>' % (
            widgets.html_params(**options), widgets.core.escape(unicode(label))
        ))


class SelectMultipleFieldWithDisable(SelectMultipleField):
    widget = SelectWithDisable(multiple=True)

    def iter_choices(self):
        for value, label, selected, disabled in self.choices:
            yield (value, label, selected, disabled)


class SelectFieldWithDisable(SelectField):
    widget = SelectWithDisable()

    def iter_choices(self):
        for value, label, selected, disabled in self.choices:
            yield (value, label, selected, disabled)


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    auth_type = SelectField('Authentication Type', validators=[DataRequired()],
                            choices=[('ldap', 'LDAP'),
                                     ('password', 'Password')])


class CreateTimeForm(Form):
    duration = StringField('Duration: (Format: #h#m, e.g. 1h15m)', validators=[DataRequired()])
    project = SelectFieldWithDisable('Project:', choices=[],
                                     validators=[DataRequired()])
    date_worked = DateField('Date Worked:', format='%Y-%m-%d',
                            description='yyyy-mm-dd',
                            validators=[DataRequired()])

    # Optional
    activities = SelectMultipleFieldWithDisable('Activities:')
    notes = StringField('Notes:')
    issue_uri = StringField('Issue URI:',
                            description='E.g. http://www.github.com')


class FilterTimesForm(Form):
    # All optional
    users = SelectMultipleFieldWithDisable('User:')
    projects = SelectMultipleFieldWithDisable('Project Slugs:')
    activities = SelectMultipleFieldWithDisable('Activity Slugs:')
    start = DateField('Start Date:', format="%Y-%m-%d",
                      description='yyyy-mm-dd', validators=[Optional()])
    end = DateField('End Date:', format="%Y-%m-%d",
                    description='yyyy-mm-dd', validators=[Optional()])
    include_deleted = BooleanField('Include Deleted', validators=[Optional()])
    include_revisions = BooleanField('Include Revisions',
                                     validators=[Optional()])


class CreateActivityForm(Form):
    name = StringField('Activity Name:', validators=[DataRequired()])
    slug = StringField('Activity Slug:', validators=[DataRequired()])


class CreateProjectForm(Form):
    uri = StringField('URI:', validators=[URL()])
    name = StringField('Name:')
    slugs = StringField('Slugs:')
    default_activity = SelectFieldWithDisable("Default Activity:")
    members = SelectMultipleFieldWithDisable('Members')
    managers = SelectMultipleFieldWithDisable('Managers')
    spectators = SelectMultipleFieldWithDisable('Spectators')


class FilterProjectsForm(Form):
    username = StringField('Username:')
    slug = StringField('Slug:')
    include_deleted = BooleanField('Include Deleted')
    include_revisions = BooleanField('Include Revisions')


class FilterActivitiesForm(Form):
    # Optional
    slug = StringField('Activity Slug:')
    include_deleted = BooleanField('Include Deleted', validators=[Optional()])
    include_revisions = BooleanField('Include Revisions',
                                     validators=[Optional()])


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
