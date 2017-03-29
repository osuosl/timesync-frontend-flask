import unittest
from flask import url_for
from tests.util import setUp, tearDown, login


class IndexPageTestCase(unittest.TestCase):

    def setUp(self):
        setUp(self)

    def tearDown(self):
        tearDown(self)

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
        bad_links = ['Logout', 'Submit Time', 'View Times', 'Admin']

        res = self.client.get(url_for('index'))

        assert link in res.get_data()

        for bad_link in bad_links:
            assert bad_link not in res.get_data()

    def test_menu_links(self):
        """Tests the index page for correct menu links."""
        login(self)

        links = ['Login', 'Logout', 'Submit Time', 'View Times']
        bad_link = 'Admin'  # Test user shouldn't see link

        res = self.client.get(url_for('index'))
        assert bad_link not in res.get_data()

        for link in links:
            assert link in res.get_data()
