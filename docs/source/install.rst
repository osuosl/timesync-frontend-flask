.. _install:

Timesync-Frontend-Flask - Web Frontend for Timesync
===================================================

.. contents::

This frontend for the `OSU Open Source Lab's`_ `Timesync API`_ uses `Pymesync`_
and the `Flask microframework`_

.. _OSU Open Source Lab's: http://www.osuosl.org/
.. _Timesync API: http://timesync.readthedocs.org/en/latest/
.. _Pymesync: http://pymesync.readthedocs.org/en/latest/
.. _Flask microframework: http://flask.pocoo.org/

Getting Timesync-Frontend-Flask
-------------------------------

To obtain a copy of the source code and set up a development environment,
first clone the `Github repo`_. After cloning the repo, run this command to
create a copy of the configuration file:

.. code-block:: none

    $ cp config.py.dist config.py

If you want to use Python virtualenvs,
follow `this tutorial`_ to set it up then run the following command in a
virtualenv:

.. code-block:: none

    (venv) $ pip install -r requirements.txt

To set up a development environment with Docker, you must have both
`docker`_ and `docker-compose`_ installed on your system. Then, with the
docker daemon running, run the following command to build the container:

.. code-block:: none

    $ docker-compose build

.. _Github repo: https://github.com/osuosl/timesync-frontend-flask
.. _this tutorial: http://docs.python-guide.org/en/latest/dev/virtualenvs
.. _docker: http://www.docker.com/
.. _docker-compose: https://docs.docker.com/compose/

Configuring Timesync-Frontend-Flask
-----------------------------------

===================== =========================================================
     Option Name                             Description
===================== =========================================================
DEBUG                 Set to :code:`True` to enable the built-in Flask debugger
TESTING               Used by unit tests for testing convenience. **Do not set**
BASE_DIR              Path to the project directory
SECRET_KEY            Secret key used to generate CSRF tokens
ENCRYPTION_KEY        Encryption key used to encrypt server-side sessions
INITIALIZATION_VECTOR Initialization vector used with the encryption key
SESSION_TYPE          Type of session store used by Flask-Session
CACHE_EXP             Number of minutes before the session cache expires
HOST                  Server Host IP
PORT                  Server Port
TIMESYNC_URL          URL of the TimeSync server to be used
===================== =========================================================

Running Timesync-Frontend-Flask
-------------------------------

To run the app without a Docker container, use

.. code-block:: none

    (venv) $ python run.py

To start it inside a Docker container, instead use

.. code-block:: none

    $ docker-compose up

Once the app is running, you can access the main page at the host IP and port
set in config.py. If these values haven't been set, they default to "localhost"
and "5000" and you can find the index page at **http://localhost:5000**.
