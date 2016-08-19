import datetime
import random
import time
import pymesync

ts = pymesync.TimeSync(baseurl='http://timesync-node:8000/v0')
ts.authenticate(username='admin', password='admin', auth_type='password')

dummy_users = [('Alice', 'alice'), ('Bob', 'bob'), ('John', 'john'), ('Mary', 'mary')]
existing_users = [u['username'] for u in ts.get_users()]

for display, user in dummy_users:
    if user in existing_users:
        continue

    print "Creating user {}".format(user)
    res = ts.create_user({"username": user, "password": user, "display_name": display, "email": "{}@test.com".format(user), "site_spectator": True})

    if "error" in res or "pymesync error" in res:
        print res
        break

dummy_projects = [('Project X', 'px'), ('Project Y', 'py'), ('Project Z', 'pz')]
dummy_project_permissions = {u: {"member": True, "spectator": True, "manager": False} for _, u in dummy_users}
existing_projects = [p['slugs'][0] for p in ts.get_projects()]

for name, slug in dummy_projects:
    if slug in existing_projects:
        continue

    print 'Creating project {}'.format(name)
    res = ts.create_project({"name": name, "slugs": [slug], "uri": "http://www.{}.com".format(slug), "users": dummy_project_permissions})

    if 'error' in res or 'pymesync error' in res:
        print res
        break

dummy_activities = ['development', 'testing', 'debug', 'meetings', 'design', 'planning', 'documentation']
existing_activities = [a['slug'] for a in ts.get_activities()]

for activity in dummy_activities:
    if activity in existing_activities:
        continue

    print 'Creating activity {}'.format(activity)
    res = ts.create_activity({"name": activity, "slug": activity})

    if 'error' in res or 'pymesync error' in res:
        print res
        break

for _, user in dummy_users:
    print 'Generating times for {}'.format(user)

    res = ts.authenticate(username=user, password=user, auth_type='password')

    if 'error' in res or 'pymesync error' in res:
        print res
        break

    for i in range(50):
        duration = random.randint(1, 20) * 60 * 15
        project = random.choice(dummy_projects)[1]
        activity = random.choice(dummy_activities)
        date_worked = datetime.date.fromtimestamp(random.randint(time.mktime(datetime.date(2013, 1, 1).timetuple()), time.mktime(datetime.date(2017, 1, 1).timetuple()))).isoformat()

        res = ts.create_time({"duration": duration, "project": project, "activities": [activity], "date_worked": date_worked, "user": user})
        if 'error' in res or 'pymesync error' in res:
            print res
            break

print 'Done!'
