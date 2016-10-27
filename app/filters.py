from app import app


@app.template_filter()
def hms_filter(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return "{} h, {} m, {} s".format(h, m, s)


@app.template_filter()
def select_with_disabled(field):
    # Set 'selected' and 'disabled' to False for all fields except default
    
    for i, choice in enumerate(field.choices):
        field.choices[i] = choice + (False, False,)

    default = ('', 'Choose option(s)', True, True)
    field.choices.insert(0, default)

    return field
