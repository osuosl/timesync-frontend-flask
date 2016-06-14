from flask import render_template
from app import app
from app.util import get_user, is_logged_in


@app.route('/')
def index():
    is_admin = False
    logged_in = is_logged_in()

    if logged_in:
        user = get_user()
        if 'error' in user or 'pymesync error' in user:
            print user
            return "There was an error.", 500

        if type(user) is dict:
            is_admin = user['site_admin']

    return render_template('index.html', is_logged_in=logged_in,
                           is_admin=is_admin)
