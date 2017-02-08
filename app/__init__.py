import sys

from flask import Flask
from flask.ext.session import Session
from flask_assets import Environment, Bundle

app = Flask(__name__, static_folder="static")

try:
    app.config.from_object('config')
except ImportError as e:
    print e
    print 'Error loading configuration!'
    print 'Does the file exist?'
    sys.exit(1)

# Server-side sessions
Session(app)

# Do some config checks
if app.config.get('TIMESYNC_URL') == 'http://timesync.example.com/':
    print 'ERROR: Configuration option "TIMESYNC_URL" not set'
    print '       Please set "TIMESYNC_URL" to the URL of your TimeSync server'

if app.config.get('SECRET_KEY') == 'secret':
    print 'WARNING: "SECRET_KEY" hasn\'t been set! If you want to use CSRF'
    print '         protection, you should set it!'

if app.config.get('TESTING'):
    print 'WARNING: In testing mode, the app probably won\'t behave quite'
    print '         like you would expect it to. You have been warned!'

key = "\x1ft\xeb\xd2\xb72\x16CT\xacE\xde\xedP\xf1\xe2\xcb\x10\xfe\xb1\x12" \
      "\xac\x9d\x91$\xa4\x17\x0f\x88\\\xb2f"
if app.config.get('ENCRYPTION_KEY') == key:
    print 'WARNING: The encryption key has not been changed from the default'
    print '         This is insecure, please generate a new one'

iv = "abcdefghijklmnop"
if app.config.get('INITIALIZATION_VECTOR') == iv:
    print 'WARNING: The initialization vector has not been changed from the'
    print '         default. This is insecure, please generate a new one'

assets = Environment(app)
indexjs = Bundle('../js/index.js', filters='rjsmin', output='js/index.min.js')
formjs = Bundle('../js/clear_form.js', '../js/table_sort.js', filters='rjsmin',
                output='js/tableform.min.js')

assets.config['LIBSASS_STYLE'] = 'compressed'
css = Bundle('../css/style.scss', filters='libsass',
             output='css/style.min.css')

assets.register('index_js', indexjs)
assets.register('js_forms', formjs)
assets.register('css', css)

from app.middleware import check_cache_autoupdate  # NOQA flake8 ignore
from app.views import index, create_time, delete_time  # NOQA flake8 ignore
from app.views import login, logout, view_times, view_user_times, edit_time  # NOQA flake8 ignore
from app.views import create_project, edit_project, view_projects  # NOQA flake8 ignore
from app.views import create_activity, edit_activity, view_activities, delete_activity  # NOQA flake8 ignore
from app.views import create_user, edit_user, view_users, delete_user  # NOQA flake8 ignore
from app.util import get_user, is_logged_in, error_message  # NOQA flake8 ignore
from app.util import project_user_permissions  # NOQA flake8 ignore
from app import filters  # NOQA flake8 ignore
