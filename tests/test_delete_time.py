import unittest
from app import app
from flask import url_for
from urlparse import urlparse


class DeleteTimeTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

        self.ctx = app.test_request_context()
        self.ctx.push()

        self.baseurl = app.config['TIMESYNC_URL']

    def tearDown(self):
        self.ctx.pop()

    def login_user(self):
        self.username = 'test'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def login_admin(self):
        self.username = 'admin'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def get_page(self):
        res = self.client.get(url_for('delete_time', uuid='test'))

        return res

    def delete_time(self):
        res = self.client.post(url_for('delete_time'), data=dict(
            uuid="test"
        ), follow_redirects=True)

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for delete_time exists"""
        url = url_for('delete_time')
        assert url == '/times/delete'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login_admin()

        res = self.get_page()
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure users who aren't logged in are redirected to log in"""
        res = self.get_page()
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_access_denied(self):
        """Make sure unauthorized users are denied access"""
        self.login_user()
        res = self.get_page()

        assert res.status_code == 500
