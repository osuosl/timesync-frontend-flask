import unittest
from app import app
from flask import url_for
from urlparse import urlparse
import pymesync


class DeleteActivityTestCase(unittest.TestCase):

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
        res = self.client.get(url_for('delete_activity', slug='test'))

        return res

    def get_page_no_slug(self):
        res = self.client.get(url_for('delete_activity'))

        return res

    def delete_activity(self):
        res = self.client.post(url_for('delete_activity'), data=dict(
            ts_object="test"
        ), follow_redirects=True)

        return res

    def delete_activity_no_slug(self):
        res = self.client.post(url_for('delete_activity'), data=dict(),
                               follow_redirects=True)

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for delete_activity exists"""
        url = url_for('delete_activity')
        assert url == '/activities/delete'

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

        assert 'activity-info' in page_data
        assert 'confirm-delete' in page_data

        ts = pymesync.TimeSync(baseurl='test', test=True)
        ts.authenticate('test', 'test', 'password')
        ref_activity = ts.get_activities({"slug": "test"})[0]

        assert ref_activity['name'] in page_data
        assert ref_activity['slug'] in page_data

    def test_get_page_no_slug(self):
        """Make sure that trying to get the page without a slug fails"""
        self.login_admin()
        res = self.get_page_no_slug()

        assert res.status_code == 404

    def test_delete_activity_admin(self):
        """Test deleting an activity as an admin"""
        self.login_admin()
        res = self.delete_activity()

        assert 'Deletion successful' in res.data

    def test_delete_activity_nonadmin(self):
        """Test deleting an activity as a regular user"""
        self.login_nonadmin()
        res = self.delete_activity()

        assert res.status_code == 403

    def test_delete_activity_no_slug(self):
        """Test deleting an activity without providing a slug"""
        self.login_admin()
        res = self.delete_activity_no_slug()

        assert res.status_code == 404
