import unittest
from app import app
from flask import url_for
from urlparse import urlparse
import pymesync


class DeleteProjectTestCase(unittest.TestCase):

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
            password=self.password,
            auth_type="password"
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def login_nonadmin(self):
        self.username = 'test'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password,
            auth_type="password"
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def get_page(self):
        res = self.client.get(url_for('delete_project', slug='test'))

        return res

    def get_page_no_slug(self):
        res = self.client.get(url_for('delete_project'))

        return res

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

        assert 'project-info' in page_data
        assert 'confirm-delete' in page_data

        ts = pymesync.TimeSync(baseurl='test', test=True)
        ts.authenticate('test', 'test', 'password')
        ref_project = ts.get_projects({"slug": "test"})[0]

        assert ref_project['name'] in page_data
        assert ' '.join(ref_project['slugs']) in page_data

    def test_get_page_no_slug(self):
        """Make sure that trying to get the page without a slug fails"""
        self.login_admin()
        res = self.get_page_no_slug()

        assert res.status_code == 404

    def test_delete_project_admin(self):
        """Test deleting a project as an admin"""
        self.login_admin()
        res = self.delete_project()

        assert 'Deletion successful' in res.data

    def test_delete_project_nonadmin(self):
        """Test deleting a project as a regular user"""
        self.login_nonadmin()
        res = self.delete_project()
        print res.status_code
        print res.data

        assert res.status_code == 403

    def test_delete_project_no_slug(self):
        """Test deleting a project without providing a slug"""
        self.login_admin()
        res = self.delete_project_no_slug()

        assert res.status_code == 404
