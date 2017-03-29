import pymesync
import unittest
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login, get_page


class DeleteUserTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def delete_user(self):
        res = self.client.post(url_for('delete_user', username='test'),
                               follow_redirects=True)

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
        login(self, username='admin')
        res = get_page(self, 'delete_user', username='test')

        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure users who aren't logged in are redirected to log in"""
        res = get_page(self, 'delete_user', username='test')
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_get_page_admin(self):
        """Make sure that site admins are allowed to access the page"""
        login(self, username='admin')
        res = get_page(self, 'delete_user', username='test')

        assert res.status_code == 200

    def test_get_page_nonadmin(self):
        """Make sure the regular users are refused access"""
        login(self)
        res = get_page(self, 'delete_user', username='test')

        assert res.status_code == 403

    def test_get_page(self):
        """Make sure that the page is correct"""
        login(self, username='admin')
        res = get_page(self, 'delete_user', username='test')
        page_data = res.data

        assert 'user-info' in page_data
        assert 'confirm-delete' in page_data

        ts = pymesync.TimeSync(baseurl='test', test=True)
        ts.authenticate('test', 'test', 'password')
        ref_user = ts.get_users(username="test")[0]

        assert ref_user['display_name'] in page_data
        assert ref_user['username'] in page_data
        assert ref_user['email'] in page_data

    def test_get_page_no_username(self):
        """Make sure that trying to get the page without a username fails"""
        login(self, username='admin')
        res = get_page(self, 'delete_user')

        assert res.status_code == 404

    def test_delete_user_admin(self):
        """Test deleting an user as an admin"""
        login(self, username='admin')
        res = self.delete_user()

        assert 'Deletion successful' in res.data

    def test_delete_user_nonadmin(self):
        """Test deleting an user as a regular user"""
        login(self)
        res = self.delete_user()

        assert res.status_code == 403

    def test_delete_user_no_username(self):
        """Test deleting an user without providing a username"""
        login(self, username='admin')
        res = self.delete_user_no_username()

        assert res.status_code == 404
