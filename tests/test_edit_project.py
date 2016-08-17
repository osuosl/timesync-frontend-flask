import unittest
from app import app
from flask import url_for
from urlparse import urlparse


class SubmitTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

        # Application context
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def not_admin_login(self):
        self.username = 'test'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password,
            auth_type="password"
        ), follow_redirects=True)

        # Get session object
        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def admin_login(self):
        self.username = 'admin'
        self.password = 'timesync-staging'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password,
            auth_type="password"
        ), follow_redirects=True)

        # Get session object
        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def submit(self):
        res = self.client.post(url_for('edit_project'), data=dict(
            uri="http://github.com",
            name="Github",
            slugs="git, hub, gh",
            users="{'tschuy': {'member': True, 'spectator': False, 'manager': \
                True}}"
        ), follow_redirects=True)
        print res
        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for submit exists."""
        url = url_for('edit_project')
        assert url == '/projects/edit/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.admin_login()

        res = self.client.get(url_for('edit_project'))
        assert res.status_code == 200

    def test_non_admin_response(self):
        """Make sure non-admins can't access projects they're not in"""
        self.not_admin_login()

        res = self.client.get(url_for('edit_project'))
        assert res.status_code == 403

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page."""
        submitRes = self.client.get(url_for('edit_project'))
        endpoint = urlparse(submitRes.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the submit page for correct form fields."""
        self.admin_login()

        res = self.client.get(url_for('edit_project'))
        fields = ['uri', 'name', 'slugs', 'members', 'managers', 'spectators']

        print res.get_data()
        for field in fields:
            assert field in res.get_data()

    def test_submit(self):
        """Tests successful project submission."""
        self.admin_login()
        res = self.submit()

        assert res.status_code == 200

    def test_unauthorized_submit(self):
        """Tests submission without logging in first."""
        res = self.submit()

        assert res.status_code == 401
