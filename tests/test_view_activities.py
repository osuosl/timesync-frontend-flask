import unittest
from app import app
from flask import url_for
from urlparse import urlparse


class ViewActivitiesTestCase(unittest.TestCase):

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

    def login_user(self):
        self.username = 'test'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for view_activities exists"""
        url = url_for('view_activities')
        assert url == '/activities'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login_admin()

        res = self.client.get(url_for('view_activities'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure people who aren't logged in are redirected to login"""
        res = self.client.get(url_for('view_activities'))
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_admin_links(self):
        """Make sure that admins can view and access the edit page"""
        self.login_admin()

        res = self.client.get(url_for('view_activities'))

        assert res.status_code == 200
        assert url_for('edit_activity') in res.data

    def test_unauthorized_user(self):
        """Make sure unauthorized users can view, but not edit"""
        self.login_user()

        res = self.client.get(url_for('view_activities'))

        assert res.status_code == 200
        assert url_for('edit_activity') not in res.data