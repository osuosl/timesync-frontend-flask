import unittest
from app import app
from flask import url_for
from urlparse import urlparse


class SubmitTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

        self.client = app.test_client()

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
        url = url_for('edit_activities')
        assert url == '/activities/edit'

    def test_success_response(self):
        """Make sure the page responds with '200 OK'"""
        self.login()

        res = self.client.get(url_for('edit_activities'))
        assert res.status_code == 200

    def test_login_redirect(self):
        """Make sure unauthorized users are redirected to login page."""
        submitRes = self.client.get(url_for('edit_activities'))
        endpoint = urlparse(submitRes.location).path

        assert endpoint == url_for('login')


    def test_form_fields(self):
        """Tests the submit page for correct form fields."""
        self.login()

        res = self.client.get(url_for('activities'))
        fields = ['form', 'input', 'Name', 'Slug', 'Updated Slug']

        for field in fields:
            assert field in res.get_data()

    def test_edit_activity(self):
        self.login()
        res = self.client.post(url_for('edit_activities'), 
                data=dict(name="sleeps", updated_slug="sp", slug="sleep"), 
                follow_redirects=True)

        assert res.status_code == 200

    def test_unauthorized_edit_activity(self):
        res = self.client.post(url_for('edit_activities'), 
                data=dict(name="sleeps", updated_slug="sp", slug="sleep"), 
                follow_redirects=True)

        assert res.status_code == 401
