import unittest
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login


class EditUserTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def submit(self):
        return self.client.post(url_for('edit_user'), data=dict(
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
        """Make sure the url endpoint for edit_user exists."""
        url = url_for('edit_user')
        assert url == '/users/edit/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        login(self)

        res = self.client.get(url_for('edit_user'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page."""
        edit_userRes = self.client.get(url_for('edit_user'))
        endpoint = urlparse(edit_userRes.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the edit_user page for correct form fields."""
        login(self)

        res = self.client.get(url_for('edit_user'))
        fields = ['form', 'input', 'User', 'Username', 'Password',
                  'Display Name', 'Email', 'Site Admin', 'Site Spectator',
                  'Site Manager', 'Active']

        for field in fields:
            assert field in res.get_data()

    def test_edit_user(self):
        """Tests successful user submission."""
        login(self)
        res = self.submit()

        assert res.status_code == 200

    def test_unauthorized_edit_user(self):
        """Tests submission without logging in first."""
        res = self.submit()

        assert res.status_code == 401
