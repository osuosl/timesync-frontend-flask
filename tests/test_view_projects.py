import unittest
from app import app, forms
from flask import url_for
from urlparse import urlparse


class ViewProjectsTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

        # Request context
        self.ctx = app.test_request_context()
        self.ctx.push()

        self.baseurl = app.config['TIMESYNC_URL']

    def tearDown(self):
        self.ctx.pop()

    def login_nonadmin(self):
        self.username = 'test'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def login_admin(self):
        self.username = 'admin'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def view_projects(self):
        res = self.client.get(url_for('view_projects'))

        return res

    def test_url_endpoint(self):
        url = url_for('view_projects')
        assert url == '/projects'

    def test_success_response(self):
        self.login_admin()

        res = self.view_projects()
        assert res.status_code == 200

    def test_login_redirect(self):
        res = view_projects()
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_view_projects_nonadmin(self):
        self.login_nonadmin()
        
        res = self.view_projects()
        assert '/projects/edit' not in res.data
        assert '/projects/delete' not in res.data

    def test_view_projects_admin(self):
        self.login_admin()

        res = self.view_projects()
        assert '/projects/edit' in res.data
        assert '/projects/delete' in res.data
