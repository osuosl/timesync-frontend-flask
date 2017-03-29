import unittest
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login, get_page


class ViewUserTimesTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def test_url_endpoint(self):
        """Make sure the url endpoint for view_times exists."""
        url = url_for('view_user_times')
        assert url == '/times/user/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        login(self)

        res = get_page(self, 'view_user_times', username='test')
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page"""
        submit_res = get_page(self, 'view_user_times', username='test')
        endpoint = urlparse(submit_res.location).path

        assert endpoint == url_for('login')
