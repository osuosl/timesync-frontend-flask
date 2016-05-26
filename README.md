# timesync-frontend-flask

[![Build Status](https://travis-ci.org/osuosl/timesync-frontend-flask.svg?branch=develop)](https://travis-ci.org/osuosl/timesync-frontend-flask)

Front-end webapp for the TimeSync API.

To run the app, you should first edit the configuration:

1. Rename the config file from `config.py.dist` to `config.py`.
2. Change the `SECRET_KEY` to one of your own. Make it unique.
4. Change `TIMESYNC_URL` to the URL of the TimeSync instance to
communicate with.
5. If you want to run it in debug mode, make sure you set `DEBUG` to `True`.

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
