from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()],
                           render_kw={"placeholder": 'username'})
    password = PasswordField('password', validators=[DataRequired()],
                             render_kw={"placeholder": 'password'})
