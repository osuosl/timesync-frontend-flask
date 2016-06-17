import unittest
from app import app
from flask import url_for
from urlparse import urlparse


class ViewUsersTestCase(unittest.TestCase):

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

    def view_users(self):
        res = self.client.get(url_for('view_users'))

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for view_users exists"""
        url = url_for('view_users')
        assert url == '/users'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login_admin()

        res = self.view_users()
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page"""
        res = self.view_users()
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_edit_delete_links(self):
        """Make sure only admins can see the links to edit/delete users"""
        self.login_nonadmin()

        res = self.view_users()
        assert '/users/edit' not in res.data
        assert '/users/delete' not in res.data

        self.login_admin()

        res = self.view_users()
        assert '/users/edit' in res.data
        assert '/users/delete' in res.data

    def test_page_content(self):
        """Make sure that user objects actually load onto the page"""
        self.login_admin()

        res = self.view_users()
        assert 'userone' in res.data
