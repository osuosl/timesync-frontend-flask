from flask import render_template, session, redirect, url_for, request
from app import app
from app.util import is_logged_in


@app.route('/times/clock', methods=['GET', 'POST'])
def clock():
    # Check if logged in first
    if not is_logged_in():
        if request.method == 'GET':
            return redirect(url_for('login', next=request.endpoint))
        elif request.method == 'POST':
            return "Not logged in.", 401

    return render_template('clock.html', is_logged_in=True,
                           is_admin=session['user']['site_admin'])
