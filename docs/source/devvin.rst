.. _dev:

Developer Documentation for Timesync-Frontend-Flask
===================================================

.. contents::

This page includes documentation for both current and prospective devs of
timesync-frontend-flask. Welcome!

Tools and Libraries
-------------------

This is a complete list of external tools that timesync-frontend-flask uses as well
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



Style Guidelines
----------------

This codebase adheres to the `PEP 8`_ standard. Make sure your code
passes inspection by :code:`flake8` before you submit a pull request!

.. _PEP 8: https://www.python.org/dev/peps/pep-0008/
