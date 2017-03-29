import unittest
from flask import url_for
from urlparse import urlparse
from tests.util import setUp, tearDown, login


class SubmitTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def submit(self):
        return self.client.post(url_for('create_project'), data=dict(
            uri="http://github.com",
            name="Github",
            slugs="git, hub, gh",
            default_activity="development",
            users="{'tschuy': {'member': True, 'spectator': False, 'manager': \
                True}}"
        ), follow_redirects=True)

    def test_url_endpoint(self):
        """Make sure the url endpoint for submit exists."""
        url = url_for('create_project')
        assert url == '/projects/create/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        login(self)

        res = self.client.get(url_for('create_project'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page."""
        submitRes = self.client.get(url_for('create_project'))
        endpoint = urlparse(submitRes.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the submit page for correct form fields."""
        login(self)

        res = self.client.get(url_for('create_project'))
        fields = ['form', 'input', 'URI', 'Name', 'Slugs', 'Default Activity',
                  'Members', 'Managers', 'Spectators']

        for field in fields:
            assert field in res.get_data()

    def test_submit(self):
        """Tests successful time submission."""
        login(self)
        res = self.submit()

        assert res.status_code == 200

    def test_unauthorized_submit(self):
        """Tests submission without logging in first."""
        res = self.submit()

        assert res.status_code == 401
