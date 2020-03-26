import os
from setuptools import find_packages, setup

from viapy import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

REQUIREMENTS = ['requests', 'rdflib', 'cached_property', 'attrdict']
TEST_REQUIREMENTS = ['pytest', 'pytest-cov']
DJANGO_REQS = ['django>=1.11,<3.1', 'django-autocomplete-light']
DJANGO_TEST_REQS = ['pytest-django']


setup(
    name='viapy',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license='Apache License, Version 2.0',
    description='Python module for interacting with VIAF data & APIs',
    long_description=README,
    url='https://github.com/Princeton-CDH/viapy',
    install_requires=REQUIREMENTS,
    setup_requires=['pytest-runner'],
    tests_require=TEST_REQUIREMENTS,
    extras_require={
        'django': DJANGO_REQS,
        'test': TEST_REQUIREMENTS,
        'test_all': TEST_REQUIREMENTS + DJANGO_REQS + DJANGO_TEST_REQS,
        'docs': ['sphinx']
    },
    author='CDH @ Princeton',
    author_email='digitalhumanities@princeton.edu',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
