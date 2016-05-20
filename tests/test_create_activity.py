import unittest
from app import app
from app import forms
from flask import url_for
from urlparse import urlparse


class CreateActivityTestCase(unittest.TestCase):

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

    def create_activity(self):
        return self.client.post(url_for('create_activity'), data=dict(
            name='test',
            slug='test'
        ), follow_redirects=True)

    def test_url_endpoint(self):
        """Make sure the url endpoint for create_activity exists."""
        url = url_for('create_activity')
        assert url == '/create_activity'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login()

        res = self.client.get(url_for('create_activity'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page."""
        res = self.client.get(url_for('create_activity'))
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the submit page for correct form fields."""
        self.login()

        form = forms.CreateActivityForm()
        fields = ['name', 'slug']

        for field in fields:
            assert field in form.data

    def test_submit(self):
        """Tests successful time submission."""
        self.login()
        res = self.create_activity()

        assert res.status_code == 200

    def test_unauthorized_submit(self):
        """Tests submission without logging in first."""
        res = self.create_activity()

        assert res.status_code == 401
