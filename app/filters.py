from app import app


@app.template_filter()
def hms_filter(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return "{} h, {} m, {} s".format(h, m, s)


@app.template_filter()
def perm_filter(permissions):
    if not permissions:
        return ''

    perm_strings = []

    for (user, roles) in permissions.iteritems():
        user_perms = ' '.join(role for role in roles if roles[role])
        perm_strings.append('{}: {}'.format(user, user_perms))

    return perm_strings
