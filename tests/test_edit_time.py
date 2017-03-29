import unittest
from app import forms
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login


class EditTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def edit(self):
        return self.client.post(url_for('edit_time', uuid='test'), data={
            "date_worked": '2016-05-20'
        }, follow_redirects=True)

    def test_url_endpoint(self):
        """Make sure the url endpoint for edit exists."""
        url = url_for('edit_time', uuid='test')
        assert url == '/times/edit/test'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        login(self, username='userone')

        res = self.client.get(url_for('edit_time', uuid='test'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page"""
        edit_res = self.client.get(url_for('edit_time', uuid='test'))
        endpoint = urlparse(edit_res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the edit page for correct form fields"""
        form = forms.CreateTimeForm()

        fields = ['duration', 'project', 'date_worked', 'activities',
                  'notes', 'issue_uri']

        for field in fields:
            assert field in form.data

    def test_edit(self):
        """Tests successful update"""
        login(self, username='userone')
        res = self.edit()

        assert res.status_code == 200
