import unittest
from app import app
from flask import url_for
from urlparse import urlparse


class CreateUserTestCase(unittest.TestCase):

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

    def submit(self):
        return self.client.post(url_for('create_user'), data=dict(
            username="test",
            password="password",
            display_name="test",
            email="test@test.com",
            site_admin=True,
            site_spectator=True,
            site_manager=True,
            active=True
        ), follow_redirects=True)

    def test_url_endpoint(self):
        """Make sure the url endpoint for create_user exists."""
        url = url_for('create_user')
        assert url == '/users/create/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login()

        res = self.client.get(url_for('create_user'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page."""
        create_userRes = self.client.get(url_for('create_user'))
        endpoint = urlparse(create_userRes.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the create_user page for correct form fields."""
        self.login()

        res = self.client.get(url_for('create_user'))
        fields = ['form', 'input', 'Username', 'Password', 'Display Name',
                  'Email', 'Site Admin', 'Site Spectator', 'Site Manager',
                  'Active']

        for field in fields:
            assert field in res.get_data()

    def test_create_user(self):
        """Tests successful time submission."""
        self.login()
        res = self.submit()

        assert res.status_code == 200

    def test_unauthorized_create_user(self):
        """Tests submission without logging in first."""
        res = self.submit()

        assert res.status_code == 401
