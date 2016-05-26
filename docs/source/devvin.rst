.. _dev:

Developer Documentation for Timesync-Frontend-Flask
===================================================

.. contents::

This page includes documentation for both current and prospective devs of
timesync-frontend-flask. Welcome!

Tools and Libraries
-------------------

This is a complete list of tools that timesync-frontend-flask uses as well
as brief descriptions of their use and links to in-depth tutorials.

Flask
'''''

`Flask`_ is a Python microframework for web development that is easy to use
and integrates well with a number of other web development tools. We use it
to handle HTTP requests and serve dynamic web pages.

.. _Flask: http://flask.pocoo.org/docs/0.10/

Jinja2
''''''

`Jinja2`_ is the template engine that we use to generate web pages. It's
the default template engine used by Flask and its syntax is very similar to
that of Python. 

.. _Jinja2: http://jinja.pocoo.org/docs/dev/

WTForms
'''''''

`WTForms`_ is the library we use to create and handle HTML forms. It provides
neat features like form validation and `CSRF`_ protection. The Flask-WTF
allows for easy integration with Flask.

.. _WTForms: http://wtforms.readthedocs.io/en/latest/index.html
.. _CSRF: https://www.owasp.org/index.php/Cross-Site_Request_Forgery_%28CSRF%29

Pymesync
''''''''

`Pymesync`_ is a Python module developed by the Open Source Lab that provides
easy access to the `TimeSync API`_. We use it to make requests to TimeSync and
receive data back from it.

.. _Pymesync: http://pymesync.readthedocs.org/en/latest/
.. _TimeSync API: http://timesync.readthedocs.org/en/latest/

High-Level Design
-----------------

Views
'''''

Flask apps are split into *views*. Each view handles a specific URL endpoint.

For example, the `login` view handles the `/login` endpoint and it supports
the `GET` and `POST` methods. If `GET` request is sent to the endpoint, the `login`
view renders a template containing an HTML form with username and password fields 
for the user to enter their credentials.

When the user submits the form. a `POST` request
is sent to the `/login` endpoint containing the user's login credentials. The
`login` view then handles the `POST` request by taking the login credentials
and sending them to TimeSync. After that, the `login` view might redirect the user
to the index page (The `/` endpoint).

Each view corresponds to a different TimeSync action 
(Adding/Updating/Viewing/Deleting times/projects/activities/users). However,
the pages to Add/Update/Delete projects/activities/users are restricted to site
admins only, and the only users who are allowed to update times are the same users
that submitted the time.

The Session
'''''''''''

Flask sessions are used to store persistent information such as TimeSync tokens
and user-specific project permissions. Session objects persist on the server side,
although TimeSync tokens are set to expire 30 minutes after they are issued.

Session encryption is currently a work-in-progress.

Template Layout
'''''''''''''''

Every template that is used in this project should inherit from the master
template in :code:`app/templates/layout.html`.

A brief description of what each block does:

========== ===============================================
Block Name                   Description
========== ===============================================
title      The page title as it appears in the web browser
imports    Non-script imports such as stylesheets
scripts    Both imported scripts and inline scripts
body       The body of the webpage
========== ===============================================

Other static page elements go in the :code:`app/static/` folder.

Style Guidelines
----------------

This codebase adheres to the `PEP 8`_ standard. Make sure your code
passes inspection by :code:`flake8` before you submit a pull request!

.. _PEP 8: https://www.python.org/dev/peps/pep-0008/

Testing
-------

Writing comprehensive unit tests is good practice. All of the tests for
timesync-frontend-flask are located in the :code:`tests/` directory, and you can run
them all at once by running :code:`nosetests` inside the project root directory.
