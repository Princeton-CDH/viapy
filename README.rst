viapy
=====

.. sphinx-start-marker-do-not-remove

*VIAF via Python*

Python module for interacting with `VIAF`_ (the Virtual International
Authority File) data and APIs.

.. _VIAF: http://viaf.org

**viapy** provides optional Django integration; this currently includes a
django-autocomplete-light lookup view and a VIAF url widget.

Python 3.5 / Django 1.11

.. image:: https://travis-ci.org/Princeton-CDH/viapy.svg?branch=master
    :target: https://travis-ci.org/Princeton-CDH/viapy
    :alt: Build status

.. image:: https://codecov.io/gh/Princeton-CDH/viapy/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/Princeton-CDH/viapy/branch/master
    :alt: Code coverage

.. image:: https://landscape.io/github/Princeton-CDH/viapy/master/landscape.svg?style=flat
   :target: https://landscape.io/github/Princeton-CDH/viapy/master
   :alt: Code Health

.. image:: https://requires.io/github/Princeton-CDH/viapy/requirements.svg?branch=master
     :target: https://requires.io/github/Princeton-CDH/viapy/requirements/?branch=master
     :alt: Requirements Status



Installation
------------

Use pip to install from GitHub.  Use a branch or tag name, e.g.
``@develop`` or ``@1.0`` if you want to install a specific tagged release or branch::

    pip install git+https://github.com/Princeton-CDH/viapy.git@develop#egg=viapy


Configuration for use with Django
---------------------------------

Using `viapy` with Django requires additional configuration.  Add `viapy` to
installed applications along with the needed django-autocomplete-light
modules::

    INSTALLED_APPS = (
        ...
        'dal',
        'dal_select2',
        'viapy',
        ...
    )


Include the viapy urls at the desired base url with the namespace::

    urlpatterns = [
        ...
        url(r'^viaf/', include('viapy.urls', namespace='viaf')),
        ...
    ]


Development instructions
------------------------

This git repository uses `git flow`_ branching conventions.

.. _git flow: https://github.com/nvie/gitflow

Initial setup and installation:

- Recommended: create and activate a python 3.5 virtualenv::

    virtualenv viapy -p python3.5
    source viapy/bin/activate

- pip install the package with its python dependencies::

    pip install -e .
    pip install -e ".[django]""


Unit Testing
^^^^^^^^^^^^

Unit tests are set up to be run with `py.test <http://doc.pytest.org/>`_

- Copy sample test settings and add a **SECRET_KEY**::

    cp ci/testsettings.py testsettings.py

- To run the tests, either use the configured setup.py test command::

    python setup.py test

- Or install test requirements and use py.test directly::

    pip install -e '.[test_all]'
    py.test


Documentation
^^^^^^^^^^^^^

Documentation is generated using `sphinx <http://www.sphinx-doc.org/>`_.
To generate documentation, first install development requirements::

    pip install -e ".[docs]"

Then build the documentation using the customized make file in the `docs`
directory::

    cd sphinx-docs
    make html

When building documentation for a production release, use `make docs` to
update the published documentation on GitHub Pages.



License
-------

**viapy** is distributed under the Apache 2.0 License.

©2017 Trustees of Princeton University.  Permission granted via
Princeton Docket #18-3449-1 for distribution online under a standard Open Source
license.  Ownership rights transferred to Rebecca Koeser provided software
is distributed online via open source.
