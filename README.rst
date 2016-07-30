monitoring-plugins-python
=========================

.. image:: https://travis-ci.org/Temelio/monitoring-plugins-python.svg?branch=master
    :target: https://travis-ci.org/Temelio/monitoring-plugins-python

Python monitoring plugins, can be used with Shinken, Nagios, Icinga, ...


Dependencies
============

Dependencies are managed by `Pip <https://pypi.python.org/pypi/pip>`_, so
thanks to follow its documentation and install it.

You should use virtualenv when you work to your project, because you'll have a
dedicated and clean environment for your project.

Just a warning about virtualenv, if you have error on python3 virtualenv
create, update the virtualenv package::

    $ pip install virtualenv --user --upgrade

Virtualenv management
---------------------
* Using virtualenv::

    $ virtualenv ./ && source ./bin/activate

* Using `pew <https://github.com/berdario/pew>`_::

    $ pew new monitoring_plugins

Install dependencies
--------------------
* With dev dependencies::

    $ pip install -r requirements_dev.txt

* Without dev dependencies::

    $ pip install -r requirements.txt


Testing
=======

Tests are automatically runned by Jenkins when you push or submit a merge
request but you must run them before push your changes to Github !

Run linter
----------

This test check syntax error and pip8 rules::

    $ make lint

Run unit tests and coverage
---------------------------

* For default python version::

    $ make test

* For all managed python version::

    $ make test-all


Documentation
=============

The documentation is self generated from code comments, following the
`RST <http://docutils.sourceforge.net/rst.html>`_ syntax and is built with
`Sphynx <http://www.sphinx-doc.org/en/stable/>`_.
Take time to read their documentation.

In fact, no comment = no documentation = **Merge request refused !**.

Generate the documentation
--------------------------

Build documentation using RST files and doctrings::

    $ make docs

You will find the generated documentation into build/doc folder.
