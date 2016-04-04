from flask import Flask

app = Flask(__name__)

try:
    app.config.from_object('config')
except:
    app.config.from_pyfile('../config.py.dist')

from app import views  # NOQA flake8 ignore
