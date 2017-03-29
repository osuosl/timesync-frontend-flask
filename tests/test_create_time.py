import unittest
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login


class SubmitTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def create_time(self):
        return self.client.post(url_for('create_time'), data=dict(
            user="test",
            duration="3",
            project="timesync-node",
            date_worked="2016-02-22"
        ), follow_redirects=True)

    def test_url_endpoint(self):
        """Make sure the url endpoint for submit exists."""
        url = url_for('create_time')
        assert url == '/times/create/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        login(self)

        res = self.client.get(url_for('create_time'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page."""
        res = self.client.get(url_for('create_time'))
        endpoint = urlparse(res.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the submit page for correct form fields."""
        login(self)

        res = self.client.get(url_for('create_time'))
        fields = ['Duration', 'Project',
                  'Activities', 'Date Worked', 'Notes', 'Issue URI']

        for field in fields:
            assert field in res.get_data()

    def test_submit(self):
        """Tests successful time submission."""
        login(self)
        res = self.create_time()

        assert res.status_code == 200

    def test_unauthorized_submit(self):
        """Tests submission without logging in first."""
        res = self.create_time()

        assert res.status_code == 401
