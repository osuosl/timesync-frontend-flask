import unittest
from app import app
from flask import url_for
from urlparse import urlparse


class SubmitTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

        # Application context
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def login(self):
        self.username = 'test'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password,
            auth_type="password"
        ), follow_redirects=True)

        # Get session object
        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def create_time(self):
        return self.client.post(url_for('create_time'), data=dict(
            user="test",
            duration="3",
            project="timesync-node",
            date_worked="2016-02-22"
        ), follow_redirects=True)

    def test_url_endpoint(self):
        """Make sure the url endpoint for submit exists."""
        url = url_for('create_time')
        assert url == '/times/create/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login()

        res = self.client.get(url_for('create_time'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page."""
        res = self.client.get(url_for('create_time'))
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the submit page for correct form fields."""
        self.login()

        res = self.client.get(url_for('create_time'))
        fields = ['Duration', 'Project',
                  'Activities', 'Date Worked', 'Notes', 'Issue URI']

        for field in fields:
            assert field in res.get_data()

    def test_submit(self):
        """Tests successful time submission."""
        self.login()
        res = self.create_time()

        assert res.status_code == 200

    def test_unauthorized_submit(self):
        """Tests submission without logging in first."""
        res = self.create_time()

        assert res.status_code == 401
