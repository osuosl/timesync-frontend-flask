import sys

from flask import Flask

app = Flask(__name__, static_folder="static")

try:
    app.config.from_object('config')
except ImportError as e:
    print e
    print 'Error loading configuration!'
    print 'Does the file exist?'
    sys.exit(1)

# Do some config checks
if app.config.get('TIMESYNC_URL') == 'http://timesync.example.com/':
    print 'ERROR: Configuration option "TIMESYNC_URL" not set'
    print '       Please set "TIMESYNC_URL" to the URL of your TimeSync server'
    sys.exit(1)

if app.config.get('SECRET_KEY') == 'secret':
    print 'WARNING: "SECRET_KEY" hasn\'t been set! If you want to use session'
    print '         encryption, you should set it!'

if app.config.get('TESTING'):
    print 'WARNING: In testing mode, the app probably won\'t behave quite'
    print '         like you would expect it to. You have been warned!'

from app.views import index, admin, create_time, delete_time  # NOQA flake8 ignore
from app.views import login, logout, view_times, edit_time  # NOQA flake8 ignore
from app.views import create_activity, edit_activity, view_activities  # NOQA flake8 ignore
from app.views import create_user, edit_user, view_users, delete_user  # NOQA flake8 ignore
from app.views import create_project, edit_project, view_projects  # NOQA flake8 ignore
from app.util import get_user, is_logged_in, error_message  # NOQA flake8 ignore
from app.util import project_user_permissions  # NOQA flake8 ignore
from app import filters  # NOQA flake8 ignore
