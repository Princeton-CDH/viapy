import os
import sys
from setuptools import find_packages, setup
from viapy import __version__

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

REQUIREMENTS = ['requests', 'rdflib', 'cached_property']
TEST_REQUIREMENTS = ['pytest', 'pytest-django', 'pytest-cov']
if sys.version_info < (3, 0):
    TEST_REQUIREMENTS.append('mock')


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
        'test': TEST_REQUIREMENTS,
    },
    author='CDH @ Princeton',
    author_email='digitalhumanities@princeton.edu',
    classifiers=[
        'Environment :: Web Environment',  # maybe/probably?
        # django TBD
        # 'Framework :: Django',
        # 'Framework :: Django :: 1.8',
        # 'Framework :: Django :: 1.9',
        # 'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # maybe we'll add 2.7 support if it's easy
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
