import unittest
from app import app
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


    def report(self):
        res = self.client.post(url_for('report'), data=dict(
            user=""
            project=""
            activity=""
            start=""
            end=""
            include_revisions=False
            include_deleted=False
        ), follow_redirects=True)

        return res


    def test_url_endpoint(self):
        """Make sure the url endpoint for report exists."""
        url = url_for('report')
        assert url == '/report'


    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login()

        res = self.client.get(url_for('report'))
        assert res.status_code == 200


    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page"""
        submit_res = self.client.get(url_for('report'))
        endpoint = urlparse(submit_res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the report page for correct form fields"""
        self.login()

        res = self.client.get(url_for('report'))
        fields = ['form', 'input', 'User', 'Project', 'Activity',
                  'Start', 'End', 'Include Revisions', 'Include Deleted']

        for field in fields:
            assert field in res.get_data()


    def test_report(self):
        """Tests successful time query"""
        self.login()
        res = self.report()

        assert res.status_code == 200


    def test_unauthorized_report(self):
        """Tests attempt to view times without logging in first"""
        res = self.report()

        assert res.status_code == 401
