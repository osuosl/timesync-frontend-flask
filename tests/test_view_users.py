import unittest
from app import forms
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login


class ReportTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def view_users(self):
        res = self.client.post(url_for('view_users'), data=dict(
            username="",
            metainfo="",
        ), follow_redirects=True)

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for view_users exists."""
        url = url_for('view_users')
        assert url == '/users/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        login(self)

        res = self.client.get(url_for('view_users'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page"""
        submit_res = self.client.get(url_for('view_users'))
        endpoint = urlparse(submit_res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the view_users page for correct form fields"""
        form = forms.FilterUsersForm()

        fields = ['username', 'metainfo']

        for field in fields:
            assert field in form.data

    def test_report(self):
        """Tests successful user query"""
        login(self)
        res = self.view_users()

        assert res.status_code == 200
