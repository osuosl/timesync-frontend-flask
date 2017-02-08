from flask import session
from app import app
from datetime import datetime
from util import build_cache, is_logged_in


@app.before_request
def check_cache_autoupdate():
    if is_logged_in() and datetime.now() >= session["next_update"]:
        build_cache()
