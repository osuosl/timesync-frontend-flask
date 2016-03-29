# timesync-frontend-flask

[![Build Status](https://travis-ci.org/osuosl/timesync-frontend-flask.svg?branch=develop)](https://travis-ci.org/osuosl/timesync-frontend-flask)

Front-end webapp for the TimeSync API.

To install requirements, do:
```sh
$ virtualenv venv -p python2
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

To run the app, you should first edit the configuration:

1. Rename the config file from `config.py.dist` to `config.py`.
2. Change the `SECRET_KEY` to one of your own. Make it unique.
4. Change `TIMESYNC_URL` to the URL of the TimeSync instance to
communicate with.
5. If you want to run it in debug mode, make sure you set `DEBUG` to `True`.

To run tests, do:
```
(venv) $ nosetests
```
