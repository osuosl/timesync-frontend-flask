from app import app


@app.template_filter()
def hms_filter(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return "{} h, {} m, {} s".format(h, m, s)


@app.template_filter()
def bool_filter(value):
    return 'Y' if value else 'N'
