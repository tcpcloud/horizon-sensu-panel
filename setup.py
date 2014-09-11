#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import horizon_monitoring

PACKAGE_NAME = 'robotice'
PACKAGE_DIR = 'robotice'

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    author='Ales Komarek & Michael Kuty',
    author_email='mail@newt.cz & mail@majklk.cz',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Distributed Environment',
        'Framework :: Openstack Horizon',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    description='Horizon panels integrating Sensu monitoring and KEDB database.',
    include_package_data=True,
    license=license,
    long_description=readme + '\n\n' + history,
    name=PACKAGE_NAME,
    platforms=['any'],
    url='https://github.com/tcpcloud/horizon-sensu-panel',
    version=horizon_monitoring.__version__,
    zip_safe=False,
)