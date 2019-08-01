#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError as ierr:
    print 'Import error :' + str(ierr)
    from distutils.core import setup

setup(
    name='baySerial',
    version='0.0.1',
    packages=['baySerial'],
    description='Python port of the baySerial protocoll',
    author='Stefan Holzheu',
    author_email='stefan.holzheu@bayceer.uni-bayreuth.de',
    license='GPL2',
    keywords='serial bayeos',
    classifiers=['Programming Language :: Python'],
)
