import unittest
from app import forms
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login


class CreateActivityTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def create_activity(self):
        return self.client.post(url_for('create_activity'), data=dict(
            name='asdf',
            slug='asdf'
        ), follow_redirects=True)

    def test_url_endpoint(self):
        """Make sure the url endpoint for create_activity exists."""
        url = url_for('create_activity')
        assert url == '/activities/create/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        login(self, username='admin')

        res = self.client.get(url_for('create_activity'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page."""
        res = self.client.get(url_for('create_activity'))
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the submit page for correct form fields."""
        login(self, username='admin')

        form = forms.CreateActivityForm()
        fields = ['name', 'slug']

        for field in fields:
            assert field in form.data

    def test_submit(self):
        """Tests successful time submission."""
        login(self, username='admin')
        res = self.create_activity()

        assert res.status_code == 200

    def test_unauthorized_submit(self):
        """Tests submission without logging in first."""
        login(self)
        res = self.create_activity()

        assert res.status_code == 401
