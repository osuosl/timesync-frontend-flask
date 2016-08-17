import unittest
from app import app, forms
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
            password=self.password,
            auth_type="password"
        ), follow_redirects=True)

        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def login_user(self):
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

    def get_view_activities(self):
        res = self.client.get(url_for('view_activities'))

        return res

    def view_activities(self):
        res = self.client.post(url_for('view_activities'), data={
            "slug": "testslug"
        })

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for view_activities exists"""
        url = url_for('view_activities')
        assert url == '/activities/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login_admin()

        res = self.get_view_activities()
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure people who aren't logged in are redirected to login"""
        res = self.get_view_activities()
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Make sure that the FilterActivitesForm has the correct fields"""
        form = forms.FilterActivitiesForm()

        fields = ['slug']

        for field in fields:
            assert field in form.data

    def test_page_layout(self):
        """Make sure that the proper divs are on the page"""
        self.login_user()

        res = self.get_view_activities()

        assert 'filter-params' in res.data
        assert 'view-activities' in res.data

    def test_submit_filter_form(self):
        """Make sure that the filter form functions properly"""
        self.login_user()

        res = self.view_activities()

        assert 'testslug' in res.data

    def test_admin_links(self):
        """Make sure that admins can view and access the edit page"""
        self.login_admin()

        res = self.get_view_activities()

        assert res.status_code == 200
        assert url_for('edit_activity') in res.data

    def test_unauthorized_user(self):
        """Make sure unauthorized users can view, but not edit"""
        self.login_user()

        res = self.get_view_activities()

        assert res.status_code == 200
        assert url_for('edit_activity') not in res.data
