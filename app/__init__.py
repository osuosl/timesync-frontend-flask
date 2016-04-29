from flask import Flask
from redis import StrictRedis

app = Flask(__name__)
app.config.from_object('config')

redis = StrictRedis(host='redis')

from app import views  # NOQA flake8 ignore
