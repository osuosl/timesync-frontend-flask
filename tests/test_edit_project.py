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
        res = self.client.post(url_for('edit_project'), data=dict(
            uri="http://github.com",
            name="Github",
            slugs="git, hub, gh",
            default_activity="development",
            users="{'tschuy': {'member': True, 'spectator': False, 'manager': \
                True}}"
        ), follow_redirects=True)
        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for submit exists."""
        url = url_for('edit_project')
        assert url == '/projects/edit/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        login(self, username='admin')

        res = self.client.get(url_for('edit_project'))
        assert res.status_code == 200

    def test_non_admin_response(self):
        """Make sure non-admins can't access projects they're not in"""
        login(self)

        res = self.client.get(url_for('edit_project'))
        assert res.status_code == 403

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page."""
        submitRes = self.client.get(url_for('edit_project'))
        endpoint = urlparse(submitRes.location).path

        assert endpoint == url_for('login')

    def test_form_fields(self):
        """Tests the submit page for correct form fields."""
        login(self, username='admin', password='timesync-staging')

        res = self.client.get(url_for('edit_project'))
        fields = ['uri', 'name', 'slugs', 'default_activity', 'members',
                  'managers', 'spectators']

        for field in fields:
            assert field in res.get_data()

    def test_submit(self):
        """Tests successful project submission."""
        login(self, username='admin', password='timesync-staging')
        res = self.submit()

        assert res.status_code == 200

    def test_unauthorized_submit(self):
        """Tests submission without logging in first."""
        res = self.submit()

        assert res.status_code == 401
