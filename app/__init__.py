from flask import Flask

app = Flask(__name__, static_folder="static")
app.config.from_object('config')

from app.views import index, admin, create_time  # NOQA flake8 ignore
from app.views import login, logout, view_times  # NOQA flake8 ignore
from app.views import create_activity, edit_activity, view_activities # NOQA flake8 ignore
from app.util import get_user, is_logged_in  # NOQA flake8 ignore
"""
from app.views import admin  # NOQA flake8 ignore
from app.views import create_time  # NOQA flake8 ignore
from app.views import get_user  # NOQA flake8 ignore
from app.views import is_logged_in  # NOQA flake8 ignore
from app.views import login  # NOQA flake8 ignore
from app.views import logout  # NOQA flake8 ignore
from app.views import view_times  # NOQA flake8 ignore
"""
from app import filters  # NOQA flake8 ignore
