from flask import render_template, session
from app import app
from app.util import is_logged_in


@app.route('/')
def index():
    is_admin = False
    logged_in = is_logged_in()

    if logged_in:
        user = session['user']
        if not user:
            return "There was an error.", 500

        is_admin = user['site_admin']

    return render_template('index.html', is_logged_in=logged_in,
                           is_admin=is_admin)
