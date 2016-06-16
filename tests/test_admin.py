import unittest
from app import app
from flask import url_for
from urlparse import urlparse


class AdminTestCase(unittest.TestCase):

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
            password=self.password
        ), follow_redirects=True)

        # Get session object
        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def adminLogin(self):
        self.username = 'admin'
        self.password = 'password'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        # Get session object
        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for admin exists."""
        url = url_for('admin')
        assert url == '/admin'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.adminLogin()

        res = self.client.get(url_for('admin'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page."""
        adminRes = self.client.get(url_for('admin'))
        endpoint = urlparse(adminRes.location).path

        assert endpoint == url_for('login')

    def test_unauthorized_response(self):
        """Make sure non-admin users can't access the page."""
        self.login()

        res = self.client.get(url_for('admin'))
        assert res.status_code == 401

    def test_links(self):
        """Test the admin page for correct links."""
        self.adminLogin()

        links = ['Create User', 'View Users']

        res = self.client.get(url_for('admin'))

        for link in links:
            assert link in res.get_data()
