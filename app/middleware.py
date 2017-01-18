from app import app
from util import is_logged_in, update_cache


@app.before_request
def autoupdate_cache():
    if is_logged_in():
        update_cache()
