from app import app


@app.template_filter()
def hms_filter(seconds):
    """Custom Jinja2 filter for converting a numeric time value in seconds to a
    human-readable time value"""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return "{} h, {} m, {} s".format(h, m, s)
