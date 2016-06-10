from flask import Flask

app = Flask(__name__, static_folder="static")
app.config.from_object('config')

from app.views import index  # NOQA flake8 ignore
from app.views import admin  # NOQA flake8 ignore
from app.views import create_time  # NOQA flake8 ignore
from app.views import get_user  # NOQA flake8 ignore
from app.views import is_logged_in  # NOQA flake8 ignore
from app.views import login  # NOQA flake8 ignore
from app.views import logout  # NOQA flake8 ignore
from app.views import view_times  # NOQA flake8 ignore
from app import filters  # NOQA flake8 ignore
