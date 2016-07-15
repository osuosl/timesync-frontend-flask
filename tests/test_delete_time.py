import unittest
from app import app, filters
from flask import url_for
from urlparse import urlparse
import pymesync


class DeleteTimeTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

        self.ctx = app.test_request_context()
        self.ctx.push()

        self.baseurl = app.config['TIMESYNC_URL']

    def tearDown(self):
        self.ctx.pop()

    def login_unauthorized(self):
        self.username = 'unauthorized'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def login_user(self):
        self.username = 'userone'
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

    def get_page(self):
        res = self.client.get(url_for('delete_time', time='test'))

        return res

    def get_page_no_uuid(self):
        res = self.client.get(url_for('delete_time'))

        return res

    def delete_time(self):
        res = self.client.post(url_for('delete_time'), data=dict(
            uuid="test"
        ), follow_redirects=True)

        return res

    def delete_time_no_uuid(self):
        res = self.client.post(url_for('delete_time'), data=dict(),
                               follow_redirects=True)

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for delete_time exists"""
        url = url_for('delete_time')
        assert url == '/times/delete/'

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
        """Make sure that site admins are allowed to acces the page"""
        self.login_admin()
        res = self.get_page()

        assert res.status_code == 200

    def test_get_page_user(self):
        """Make sure that users that own the time have access"""
        self.login_user()
        res = self.get_page()

        assert res.status_code == 200

    def test_get_page_unauthorized(self):
        """Make sure unauthorized users are denied access"""
        self.login_unauthorized()
        res = self.get_page()

        assert res.status_code == 500

    def test_get_page(self):
        """Make sure that the page is correct"""
        self.login_admin()
        res = self.get_page()
        page_data = res.data

        assert 'time-info' in page_data
        assert 'confirm-delete' in page_data
        assert url_for('view_times') in page_data

        ts = pymesync.TimeSync(baseurl='test', test=True)
        ts.authenticate('test', 'test', 'password')
        ref_time = ts.get_times({"uuid": "test"})[0]

        assert ref_time['uuid'] in page_data
        assert ref_time['user'] in page_data
        assert filters.hms_filter(ref_time['duration']) in page_data
        assert ref_time['date_worked'] in page_data
        assert ' '.join(ref_time['project']) in page_data
        assert ' '.join(ref_time['activities']) in page_data
        assert ref_time['issue_uri'] in page_data
        assert ref_time['notes'] in page_data

    def test_get_page_no_uuid(self):
        """Make sure that trying to get the page without a UUID fails"""
        self.login_admin()
        res = self.get_page_no_uuid()

        assert res.status_code == 404

    def test_delete_time_admin(self):
        """Test deleting a time as an admin"""
        self.login_admin()
        res = self.delete_time()

        assert 'Deletion successful' in res.data

    def test_delete_time_user(self):
        """Test deleting a time as the user that owns the time"""
        self.login_user()
        res = self.delete_time()

        assert 'Deletion successful' in res.data

    def test_delete_time_unauthorized(self):
        """Test deleting a time as an unauthorized user"""
        self.login_unauthorized()
        res = self.delete_time()

        assert res.status_code == 500

    def test_delete_time_no_uuid(self):
        """Test deleting a time without putting a UUID in the query string"""
        self.login_admin()
        res = self.delete_time_no_uuid()

        assert res.status_code == 404
