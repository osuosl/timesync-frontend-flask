import unittest
from app import app
from flask import url_for
from urlparse import urlparse


class ViewUserTimesTestCase(unittest.TestCase):

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
            password=self.password,
            auth_type="password"
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def view_user_times(self):
        res = self.client.get(url_for('view_user_times', username='test'))

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for view_times exists."""
        url = url_for('view_user_times')
        assert url == '/times/user/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login()

        res = self.view_user_times()
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page"""
        submit_res = self.view_user_times()
        endpoint = urlparse(submit_res.location).path

        assert endpoint == url_for('login')
