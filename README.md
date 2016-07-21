# timesync-frontend-flask

[![Build Status](https://travis-ci.org/osuosl/timesync-frontend-flask.svg?branch=develop)](https://travis-ci.org/osuosl/timesync-frontend-flask)

Front-end webapp for the TimeSync API.

## Configuration

Copy `config.py.dist` and rename the copy `config.py`

```sh
$ cp config.py.dist config.py
```

Inside `config.py` there are several options that **must** be set before
running the app for the first time

| Option         | Description                                               |
|:--------------:|:---------------------------------------------------------:|
| `SECRET_KEY`   | The secret encryption key used to encrypt sessions. Make sure that it's hard to guess |
| `TIMESYNC_URL` | The URL of the TimeSync server that this app will use     |

For a full list of configuration options, check out the documentation

## Development

To get set up in a development environment, you will first need to install:
- `docker`
- `docker-compose`

### Setting up the development environment

To build the docker container do:
```sh
$ docker-compose build
```

Once that's done, you can run the app using:
```sh
$ docker-compose up
```

## Production

To install requirements, do:
```sh
$ virtualenv venv -p python2
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

To start the app, do:
```
(venv) $ python run.py
```

-----

You can access the webpage at http://localhost:5000. The login page can be found
at http://localhost:5000/login. To submit a time, visit
http://localhost:5000/submit.

To run tests, do:
```
(venv) $ nosetests
```

To build documentation, do:
```
(venv) $ cd docs
(venv) $ make html
(venv) $ <browser> build/html/index.html
```
