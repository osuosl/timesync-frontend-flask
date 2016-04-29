from flask import Flask
from app import redis_wrapper

app = Flask(__name__)
app.config.from_object('config')

redis = redis_wrapper.RedisWrapper(app.config['TESTING'])

from app import views  # NOQA flake8 ignore
