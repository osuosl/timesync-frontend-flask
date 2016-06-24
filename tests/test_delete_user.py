import unittest
from app import app
from flask import url_for
from urlparse import urlparse
import pymesync


class DeleteUserTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

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

    def get_page(self):
        res = self.client.get(url_for('delete_user', username='test'))

        return res

    def get_page_no_username(self):
        res = self.client.get(url_for('delete_user'))

        return res

    def delete_user(self):
        res = self.client.post(url_for('delete_user'), data=dict(
            ts_object="test"
        ), follow_redirects=True)

        return res

    def delete_user_no_username(self):
        res = self.client.post(url_for('delete_user'), data=dict(),
                               follow_redirects=True)

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for delete_user exists"""
        url = url_for('delete_user')
        assert url == '/users/delete'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login_admin()
        res = self.get_page()

        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure users who aren't logged in are redirected to log in"""
        res = self.get_page()
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_get_page_admin(self):
        """Make sure that site admins are allowed to access the page"""
        self.login_admin()
        res = self.get_page()

        assert res.status_code == 200

    def test_get_page_nonadmin(self):
        """Make sure the regular users are refused access"""
        self.login_nonadmin()
        res = self.get_page()

        assert res.status_code == 403

    def test_get_page(self):
        """Make sure that the page is correct"""
        self.login_admin()
        res = self.get_page()
        page_data = res.data

        assert 'user-info' in page_data
        assert 'confirm-delete' in page_data

        ts = pymesync.TimeSync(baseurl='test', test=True)
        ts.authenticate('test', 'test', 'password')
        ref_user = ts.get_users(username="test")[0]

        assert ref_user['display_name'] in page_data
        assert ref_user['username'] in page_data
        assert ref_user['email'] in page_data
        #assert ref_user['site_admin'] in page_data
        #assert ref_user['site_manager'] in page_data
        #assert ref_user['site_spectator'] in page_data
        #assert ref_user['active'] in page_data

    def test_get_page_no_username(self):
        """Make sure that trying to get the page without a username fails"""
        self.login_admin()
        res = self.get_page_no_username()

        assert res.status_code == 404

    def test_delete_user_admin(self):
        """Test deleting an user as an admin"""
        self.login_admin()
        res = self.delete_user()

        assert 'Deletion successful' in res.data

    def test_delete_user_nonadmin(self):
        """Test deleting an user as a regular user"""
        self.login_nonadmin()
        res = self.delete_user()

        assert res.status_code == 403

    def test_delete_user_no_username(self):
        """Test deleting an user without providing a username"""
        self.login_admin()
        res = self.delete_user_no_username()

        assert res.status_code == 404
