from flask import session, redirect, url_for, request, render_template, flash
from app import app, forms
from datetime import datetime
import pymesync
import re

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('token', None)
    return redirect(url_for('index'))

