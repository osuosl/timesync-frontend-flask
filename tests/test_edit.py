import unittest
from app import app
from app import forms
from flask import url_for
from urlparse import urlparse


class EditTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def login(self):
        self.username = 'userone'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def edit(self):
        return self.client.post(url_for('edit'), data={
            "date_worked": '2016-05-20'
        }, follow_redirects=True)

    def test_url_endpoint(self):
        """Make sure the url endpoint for edit exists."""
        url = url_for('edit')
        assert url == '/edit'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login()

        res = self.client.get(url_for('edit'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page"""
        edit_res = self.client.get(url_for('edit'))
        endpoint = urlparse(edit_res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the edit page for correct form fields"""
        form = forms.SubmitTimesForm()

        fields = ['user', 'duration', 'project', 'date_worked', 'activities',
                  'notes', 'issue_uri']

        for field in fields:
            assert field in form.data

    def test_edit(self):
        """Tests successful update"""
        self.login()
        res = self.edit()

        assert res.status_code == 200
