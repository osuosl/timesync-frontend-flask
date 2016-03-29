DEBUG = True

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads
THREADS_PER_PAGE = 2

CSRF_ENABLED = True

# Secret keys, CHANGE THESE
CSRF_SESSION_KEY = "secret"
SECRET_KEY = "secret"