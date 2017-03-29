from app import app
from flask import url_for


def login(self, username='test', password='test'):
    self.username = username
    self.password = password

    res = self.client.post(url_for('login'), data=dict(
        username=self.username,
        password=self.password,
        auth_type="password"
    ), follow_redirects=True)

    # Get session object
    with self.client.session_transaction() as sess:
        self.sess = sess

    return res


def setUp(self):
    # Setup testing config
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    # Create test client
    self.client = app.test_client()

    # Application context
    self.ctx = app.test_request_context()
    self.ctx.push()

    # Set baseurl for pymesync
    self.baseurl = app.config['TIMESYNC_URL']


def tearDown(self):
    self.ctx.pop()


def get_page(self, url, **kwargs):
    return self.client.get(url_for(url, **kwargs))
