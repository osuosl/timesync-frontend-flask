import unittest
from app import app, forms
from flask import url_for
from urlparse import urlparse


class ReportTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

        # Application context
        self.ctx = app.test_request_context()
        self.ctx.push()

        self.baseurl = app.config['TIMESYNC_URL']

    def tearDown(self):
        self.ctx.pop()

    def login(self):
        self.username = 'test'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def view_projects(self):
        res = self.client.post(url_for('view_projects'), data=dict(
            name="",
            slugs="",
            members="",
            managers="",
            spectators="",
            include_revisions=False,
            include_deleted=False
        ), follow_redirects=True)

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for view_projects exists."""
        url = url_for('view_projects')
        assert url == '/projects/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login()

        res = self.client.get(url_for('view_projects'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page"""
        submit_res = self.client.get(url_for('view_projects'))
        endpoint = urlparse(submit_res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the view_projects page for correct form fields"""
        form = forms.FilterProjectsForm()

        fields = ['username', 'slug', 'include_deleted', 'include_revisions']

        for field in fields:
            assert field in form.data

    def test_report(self):
        """Tests successful project query"""
        self.login()
        res = self.view_projects()

        assert res.status_code == 200
