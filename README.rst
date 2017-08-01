viapy
=====

*VIAF via Python*

Python module for interacting with `VIAF`_ (the Virtual International
Authority File) data and APIs.

.. _VIAF: http://viaf.org


Development instructions
------------------------

This git repository uses `git flow`_ branching conventions.

.. _git flow: https://github.com/nvie/gitflow

Initial setup and installation:

- recommended: create and activate a python 3.5 virtualenv::

    virtualenv viapy -p python3.5
    source viapy/bin/activate

- pip install the package with its python dependencies::

    pip install -e .


Unit Testing
^^^^^^^^^^^^

Unit tests are set up to be run with [py.test](http://doc.pytest.org/)

- To run the tests, either use the configured setup.py test command::

    python setup.py test

- Or install test requirements and use py.test directly::

    pip install -e '.[test]'
    py.test



