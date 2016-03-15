import unittest
from app import app
from flask import url_for
import pymesync
import datetime


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

        # Application context
        self.ctx = app.test_request_context()
        self.ctx.push()

        self.baseurl = 'http://timesync-staging.osuosl.org/v1'

    def tearDown(self):
        self.ctx.pop()

    def login(self):
        self.username = "test"
        self.password = "test"

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        # Get session object
        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for login exists."""
        url = url_for('login')
        assert url == '/login'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        res = self.client.get(url_for('login'))
        assert res.status_code == 200

    def test_form_fields(self):
        """Tests the login page for correct form fields."""
        res = self.client.get(url_for('login'))
        fields = ['form', 'input', 'username', 'password']

        for field in fields:
            assert field in res.get_data()

    def test_login(self):
        """Tests successful login on form submission."""
        res = self.login()

        assert res.status_code == 200

    def test_session_creation(self):
        """Makes sure the login creates a session cookie."""
        self.login()

        # Make sure username and token stored in session
        assert 'username' in self.sess
        assert 'ts' in self.sess

        # Make sure username is correct
        assert self.sess['username'] == self.username

        # Make sure token is valid
        ts = pymesync.TimeSync(self.baseurl, token=self.sess['ts']['token'])
        assert type(ts.token_expiration_time()) is datetime.datetime
