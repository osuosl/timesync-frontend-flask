import pymesync
import unittest
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login, get_page


class DeleteProjectTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def delete_project(self):
        res = self.client.post(url_for('delete_project'), data=dict(
            ts_object="test"
        ), follow_redirects=True)

        return res

    def delete_project_no_slug(self):
        res = self.client.post(url_for('delete_project'), data=dict(),
                               follow_redirects=True)

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for delete_project exists"""
        url = url_for('delete_project')
        assert url == '/projects/delete'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        login(self, username='admin')
        res = get_page(self, 'delete_project', slug='test')

        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure users who aren't logged in are redirected to log in"""
        res = get_page(self, 'delete_project', slug='test')
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_get_page_admin(self):
        """Make sure that site admins are allowed to access the page"""
        login(self, username='admin')
        res = get_page(self, 'delete_project', slug='test')

        assert res.status_code == 200

    def test_get_page_nonadmin(self):
        """Make sure the regular users are refused access"""
        login(self)
        res = get_page(self, 'delete_project', slug='test')

        assert res.status_code == 403

    def test_get_page(self):
        """Make sure that the page is correct"""
        login(self, username='admin')
        res = get_page(self, 'delete_project', slug='test')
        page_data = res.data

        assert 'project-info' in page_data
        assert 'confirm-delete' in page_data

        ts = pymesync.TimeSync(baseurl='test', test=True)
        ts.authenticate('test', 'test', 'password')
        ref_project = ts.get_projects({"slug": "test"})[0]

        assert ref_project['name'] in page_data
        assert ' '.join(ref_project['slugs']) in page_data

    def test_get_page_no_slug(self):
        """Make sure that trying to get the page without a slug fails"""
        login(self, username='admin')
        res = get_page(self, 'delete_project')

        assert res.status_code == 404

    def test_delete_project_admin(self):
        """Test deleting a project as an admin"""
        login(self, username='admin')
        res = self.delete_project()

        assert 'Deletion successful' in res.data

    def test_delete_project_nonadmin(self):
        """Test deleting a project as a regular user"""
        login(self)
        res = self.delete_project()

        assert res.status_code == 403

    def test_delete_project_no_slug(self):
        """Test deleting a project without providing a slug"""
        login(self, username='admin')
        res = self.delete_project_no_slug()

        assert res.status_code == 404
