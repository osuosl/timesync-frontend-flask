from flask import Flask

app = Flask(__name__, static_folder="static")
app.config.from_object('config')

from app.views import index, admin, create_time  # NOQA flake8 ignore
from app.views import login, logout, view_times, edit_time  # NOQA flake8 ignore
from app.views import create_activity, edit_activity, view_activities  # NOQA flake8 ignore
from app.views import create_project, edit_project, view_projects  # NOQA flake8 ignore
from app.views import create_user, edit_user, view_users  # NOQA flake8 ignore
from app.util import get_user, is_logged_in, error_message  # NOQA flake8 ignore
from app import filters  # NOQA flake8 ignore
