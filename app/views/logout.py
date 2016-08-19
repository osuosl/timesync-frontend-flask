from flask import session, redirect, url_for
from app import app


@app.route('/logout/')
def logout():
    session.pop('projects', None)
    session.pop('user', None)
    session.pop('token', None)
    return redirect(url_for('index'))
