import unittest
from app import app
from flask import url_for


class IndexPageTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

        # Application context
        self.ctx = app.test_request_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def login(self):
        self.username = 'test'
        self.password = 'test'

        res = self.client.post(url_for('login'), data=dict(
            username=self.username,
            password=self.password
        ), follow_redirects=True)

        # Get session object
        with self.client.session_transaction() as sess:
            self.sess = sess

        return res

    def test_url_endpoint(self):
        """Make sure the url endpoint for index exists."""
        url = url_for('index')
        assert url == '/'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        res = self.client.get(url_for('index'))
        assert res.status_code == 200

    def test_unauthorized_menu_links(self):
        """Make sure unauthorized users can only see login link."""
        link = 'Login'
        badLinks = ['Submit', 'Reports', 'Admin']

        res = self.client.get(url_for('index'))

        assert link in res.get_data()

        for badLink in badLinks:
            assert badLink not in res.get_data()

    def test_menu_links(self):
        """Tests the index page for correct menu links."""
        self.login()

        links = ['Login', 'Submit', 'Reports']
        badLink = 'Admin'  # Test user shouldn't see link

        res = self.client.get(url_for('index'))
        assert badLink not in res.get_data()

        for link in links:
            assert link in res.get_data()
