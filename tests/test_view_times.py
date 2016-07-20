import unittest
from app import app, forms
from flask import url_for
from urlparse import urlparse


class ReportTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

        # Application context
        self.ctx = app.test_request_context()
        self.ctx.push()

        self.baseurl = app.config['TIMESYNC_URL']

    def tearDown(self):
        self.ctx.pop()

    def login(self):
        self.username = 'test'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def view_times(self, data=None):
        """Submits a POST request to filter times"""
        if not data:
            data = {
                "user": "",
                "project": "",
                "activity": "",
                "start": "",
                "end": "",
                "include_revisions": False,
                "include_deleted": False
            }

        res = self.client.post(url_for('view_times'), data=data,
                               follow_redirects=True)

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for view_times exists."""
        url = url_for('view_times')
        assert url == '/times/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login()

        res = self.client.get(url_for('view_times'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page"""
        submit_res = self.client.get(url_for('view_times'))
        endpoint = urlparse(submit_res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the view_times page for correct form fields"""
        form = forms.FilterTimesForm()

        fields = ['user', 'project', 'activity', 'start', 'end']

        for field in fields:
            assert field in form.data

    def test_report(self):
        """Tests successful time query"""
        self.login()
        res = self.view_times()

        assert res.status_code == 200

    def test_summary_exists(self):
        """Tests that the times summary exists on the page"""
        self.login()
        res = self.view_times()

        assert "<div class=\"times-summary\">" in res.data

    def test_summary_fields(self):
        """Tests that the times summary has the correct fields"""
        self.login()
        res = self.view_times()

        fields = ["Total Time", "Unique Users", "Users List",
                  "Unique Projects", "Projects List", "Unique Activities",
                  "Activities List"]

        for field in fields:
            assert field in res.data

    def test_summary_total_time(self):
        """Tests that the total time in the summary is correct"""
        self.login()
        res = self.view_times()

        # Get the line that the total time is in
        lines = res.data.split('\n')
        total_time_line = [l for l in lines if "0 h, 0 m, 39 s" in l]

        # Assert that the line exists and contains the total time
        print total_time_line
        assert total_time_line

    def test_summary_num_unique_users(self):
        """Tests that the number of unique users in the summary is correct"""
        self.login()
        res = self.view_times()

        # Get the line that the number of unique users is in
        lines = res.data.split('\n')
        unique_users_line = [l for l in lines if "3" in l]
        # Assert that the line exists and contains the number of unique users
        print "this is unique_users_line ", unique_users_line
        assert unique_users_line

    def test_summary_users_list(self):
        """Tests that the list of users in the summary is correct"""
        self.login()
        res = self.view_times()

        # Get the line of the div that the users list is in
        lines = res.data.split('\n')
        users_div_line = [l for l in lines if "Users List" in l]

        assert users_div_line

        # Get the line of the comma-separated list of users
        # i.e. userone, usertwo, etc.
        users_list_line = lines[lines.index(users_div_line[0])]
        assert users_list_line

        users_expected = ["userone", "usertwo", "userthree"]
        users_actual = [u.strip() for u in users_list_line.split(',')]

        for user in users_expected:
            # Assert that there are no duplicate users
            assert users_actual.count(user) == 1

    def test_summary_unique_projects(self):
        """Tests that the number of unique projects in the summary is
        correct"""
        self.login()
        res = self.view_times()

        # Get the line that the number of unique projects is in
        lines = res.data.split('\n')
        unique_projects_line = [l for l in lines if "2" in l]

        # Assert that the line exists and contains the number of unique
        # projects
        assert unique_projects_line

    def test_summary_projects_list(self):
        """Tests that the list of projects in the summary is correct"""
        self.login()
        res = self.view_times()

        # Get the line of the project list div
        lines = res.data.split('\n')
        projects_div_line = [l for l in lines if "Projects List" in l]

        assert projects_div_line

        # Get the line of the comma-separated list of projects
        # Since projects can have multiple slugs, all of the project's
        # slugs are separated by forward slashes
        # i.e. timesync/ts. timesync-node/tn, etc.
        projects_list_line = lines[lines.index(projects_div_line[0])]

        assert projects_list_line

        projects_expected = [['ganeti-webmgr', 'gwm'], ['timesync', 'ts']]
        projects_actual = [[s.strip() for s in p.split('/')]
                           for p in projects_list_line.split(',')]

        for project in projects_expected:
            # Assert that there are no duplicate projects
            assert projects_actual.count(project) == 1

    def test_summary_unique_activities(self):
        """Tests that the number of unique activities in the summary is
        correct"""
        self.login()
        res = self.view_times()

        # Get the line that the number of unique activities is in
        lines = res.data.split('\n')
        unique_activities_line = [l for l in lines if "3" in l]

        # Assert that the line exists and contains the number of unique
        # activities
        assert unique_activities_line

    def test_summary_activities_list(self):
        """Tests that the list of activities in the summary is correct"""
        self.login()
        res = self.view_times()

        # Get the line of the activity list div
        lines = res.data.split('\n')
        activities_div_line = [l for l in lines if "Activities List" in l]

        assert activities_div_line

        # Get the line of the comma-separated list of activities
        # i.e. code, docs, etc.
        activities_list_line = lines[lines.index(activities_div_line[0])]

        assert activities_list_line

        activities_expected = ['code', 'docs', 'planning']
        activities_actual = [a.strip for a in activities_list_line.split(',')]

        for activity in activities_expected:
            # Assert that there are no duplicate activities
            assert activities_actual.count(activity) == 1
