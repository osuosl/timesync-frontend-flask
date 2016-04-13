from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, SelectField, \
    DateField, HiddenField
from wtforms.validators import DataRequired
from urlparse import urlparse, urljoin
from flask import request, url_for, redirect


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target


class RedirectForm(Form):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class LoginForm(RedirectForm):
    username = StringField('username', validators=[DataRequired()],
                           render_kw={"placeholder": 'username'})
    password = PasswordField('password', validators=[DataRequired()],
                             render_kw={"placeholder": 'password'})


class SubmitTimesForm(Form):
    user = StringField('User:', validators=[DataRequired()])
    duration = IntegerField('Duration:', validators=[DataRequired()])
    project = SelectField('Project:', validators=[DataRequired()])
    date_worked = DateField('Date Worked:', format='%Y-%m-%d',
                            description='yyyy-mm-dd',
                            validators=[DataRequired()])

    # Optional
    activities = StringField('Activities:', description='Comma separated')
    notes = StringField('Notes:')
    issue_uri = StringField('Issue URI:',
                            description='E.g. http://www.github.com')
