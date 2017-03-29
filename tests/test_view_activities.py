import unittest
from app import forms
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login, get_page


class ViewActivitiesTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

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
        login(self, username='admin')

        res = get_page(self, 'view_activities')
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure people who aren't logged in are redirected to login"""
        res = get_page(self, 'view_activities')
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
        login(self)

        res = get_page(self, 'view_activities')

        assert 'filter-params' in res.data
        assert 'view-activities' in res.data

    def test_submit_filter_form(self):
        """Make sure that the filter form functions properly"""
        login(self)

        res = self.view_activities()

        assert 'testslug' in res.data

    def test_admin_links(self):
        """Make sure that admins can view and access the edit page"""
        login(self, username='admin')

        res = get_page(self, 'view_activities')

        assert res.status_code == 200
        assert url_for('edit_activity') in res.data

    def test_unauthorized_user(self):
        """Make sure unauthorized users can view, but not edit"""
        login(self)

        res = get_page(self, 'view_activities')

        assert res.status_code == 200
        assert url_for('edit_activity') not in res.data
