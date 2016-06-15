from flask import render_template
from app import app
from app.util import get_user, is_logged_in, error_message


@app.route('/')
def index():
    is_admin = False
    logged_in = is_logged_in()

    if logged_in:
        user = get_user()

        error_message(user)

        if type(user) is dict:
            is_admin = user['site_admin']

    return render_template('index.html', is_logged_in=logged_in,
                           is_admin=is_admin)
