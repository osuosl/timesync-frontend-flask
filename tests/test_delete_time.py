import pymesync
import unittest
from app import filters
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login, get_page


class DeleteTimeTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def delete_time(self, uuid='test'):
        res = self.client.post(url_for('delete_time', uuid=uuid),
                               follow_redirects=True)

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for delete_time exists"""
        url = url_for('delete_time', uuid='test')
        assert url == '/times/delete/test'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        login(self, username='admin')
        res = get_page(self, 'delete_time', uuid='test')

        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure users who aren't logged in are redirected to log in"""
        res = get_page(self, 'delete_time', uuid='test')
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_get_page_admin(self):
        """Make sure that site admins are allowed to acces the page"""
        login(self, username='admin')
        res = get_page(self, 'delete_time', uuid='test')

        assert res.status_code == 200

    def test_get_page_user(self):
        """Make sure that users that own the time have access"""
        login(self, username='userone')
        res = get_page(self, 'delete_time', uuid='test')

        assert res.status_code == 200

    def test_get_page_unauthorized(self):
        """Make sure unauthorized users are denied access"""
        login(self, username='unauthorized')
        res = get_page(self, 'delete_time', uuid='test')

        assert res.status_code == 500

    def test_get_page(self):
        """Make sure that the page is correct"""
        login(self, username='admin')
        res = get_page(self, 'delete_time', uuid='test')
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
        login(self, username='admin')
        res = get_page(self, 'delete_time', uuid='')

        assert res.status_code == 404

    def test_delete_time_admin(self):
        """Test deleting a time as an admin"""
        login(self, username='admin')
        res = self.delete_time()

        assert 'Deletion successful' in res.data

    def test_delete_time_user(self):
        """Test deleting a time as the user that owns the time"""
        login(self, username='userone')
        res = self.delete_time()

        assert 'Deletion successful' in res.data

    def test_delete_time_unauthorized(self):
        """Test deleting a time as an unauthorized user"""
        login(self, username='unauthorized')
        res = self.delete_time()

        assert res.status_code == 500

    def test_delete_time_no_uuid(self):
        """Test deleting a time without putting a UUID in the query string"""
        login(self, username='admin')
        res = self.delete_time(uuid='')

        assert res.status_code == 404
