import pymesync
import unittest
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login, get_page


class DeleteActivityTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

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
        login(self, username='admin')
        res = get_page(self, 'delete_activity', slug='test')

        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure users who aren't logged in are redirected to log in"""
        res = get_page(self, 'delete_activity', slug='test')
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_get_page_admin(self):
        """Make sure that site admins are allowed to access the page"""
        login(self, username='admin')
        res = get_page(self, 'delete_activity', slug='test')

        assert res.status_code == 200

    def test_get_page_nonadmin(self):
        """Make sure the regular users are refused access"""
        login(self)
        res = get_page(self, 'delete_activity', slug='test')

        assert res.status_code == 403

    def test_get_page(self):
        """Make sure that the page is correct"""
        login(self, username='admin')
        res = get_page(self, 'delete_activity', slug='test')
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
        login(self, username='admin')
        res = get_page(self, 'delete_activity')

        assert res.status_code == 404

    def test_delete_activity_admin(self):
        """Test deleting an activity as an admin"""
        login(self, username='admin')
        res = self.delete_activity()

        assert 'Deletion successful' in res.data

    def test_delete_activity_nonadmin(self):
        """Test deleting an activity as a regular user"""
        login(self)
        res = self.delete_activity()

        assert res.status_code == 403

    def test_delete_activity_no_slug(self):
        """Test deleting an activity without providing a slug"""
        login(self, username='admin')
        res = self.delete_activity_no_slug()

        assert res.status_code == 404
