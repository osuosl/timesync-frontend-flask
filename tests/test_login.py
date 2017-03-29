import datetime
import pymesync
import unittest
from flask import url_for
from tests.util import setUp, tearDown, login


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

    def logout(self):
        res = self.client.get(url_for('logout'))

        # Get session object
        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for login exists."""
        url = url_for('login')
        assert url == '/login/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        res = self.client.get(url_for('login'))
        assert res.status_code == 200

    def test_form_fields(self):
        """Tests the login page for correct form fields."""
        res = self.client.get(url_for('login'))
        fields = ['form', 'input', 'username', 'password']

        for field in fields:
            assert field in res.get_data()

    def test_login(self):
        """Tests successful login on form submission."""
        res = login(self)

        assert res.status_code == 200

    def test_session_creation(self):
        """Makes sure the login creates a session cookie."""
        login(self)

        # Make sure username and token stored in session
        assert 'user' in self.sess
        assert 'token' in self.sess

        # Make sure projects and activities are stored in user object
        assert 'projects' in self.sess['user']
        assert 'activities' in self.sess['user']

        # Make sure username is correct
        assert self.sess['user']['username'] == self.username

        # Make sure token is valid
        ts = pymesync.TimeSync(self.baseurl, token=self.sess['token'],
                               test=True)
        assert type(ts.token_expiration_time()) is datetime.datetime

    def test_invalid_login(self):
        """Tests invalid login on bad form submission."""
        res = login(self, password='')

        assert res.status_code == 401
        assert 'Invalid submission.' in res.get_data()

    def test_logout(self):
        """Tests successful logout on form submission."""
        res = self.logout()

        assert res.status_code == 302

    def test_session_destruction(self):
        """Make sure the logout removes any session cookies."""
        login(self)
        self.logout()

        assert 'username' not in self.sess
        assert 'token' not in self.sess
