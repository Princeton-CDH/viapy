viapy
=====

*VIAF via Python*

Python module for interacting with `VIAF`_ (the Virtual International
Authority File) data and APIs.

.. _VIAF: http://viaf.org


**viapy** provides optional Django integration; this currently includes a
django-autocomplete-light lookup view and a VIAF url widget.

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

Unit tests are set up to be run with [py.test](http://doc.pytest.org/)

- Copy sample test settings and add a **SECRET_KEY**::

    cp ci/testsettings.py testsettings.py

- To run the tests, either use the configured setup.py test command::

    python setup.py test

- Or install test requirements and use py.test directly::

    pip install -e '.[test]'
    py.test



