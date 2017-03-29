import unittest
from app import forms
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login


class EditActivityTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def edit_activity(self):
        return self.client.post(url_for('edit_activity', slug='test'), data={
            "name": "asdf",
            "slug": "test"
        }, follow_redirects=True)

    def test_url_endpoint(self):
        """Make sure the url endpoint for edit exists."""
        url = url_for('edit_activity')
        assert url == '/activities/edit/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        login(self, username='admin')

        res = self.client.get(url_for('edit_activity'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page"""
        edit_res = self.client.get(url_for('edit_activity'))
        endpoint = urlparse(edit_res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the edit page for correct form fields"""
        form = forms.CreateActivityForm()

        fields = ['name', 'slug']

        for field in fields:
            assert field in form.data

    def test_edit_activity(self):
        """Tests successful update"""
        login(self, username='admin')
        res = self.edit_activity()

        assert res.status_code == 200
