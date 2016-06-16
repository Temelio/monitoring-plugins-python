#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'temelio-monitoring==0.2.0',
    'nagiosplugin==1.2.4'
]

test_requirements = [
    'bumpversion==0.5.3',
    'wheel==0.23.0',
    'watchdog==0.8.3',
    'pylint==1.5.5',
    'pytest==2.9.1',
    'pytest-cov==2.2.1',
    'tox==2.1.1',
    'Sphinx==1.3.1',
    'pytest-mock==1.1.0',
    'capturer==2.1.1',
    'requests_mock==0.7.0',
]

setup(
    name='monitoring_plugins',
    version='0.1.0',
    description=('Python monitoring plugins, can be used with Shinken, Nagios,'
                 'Icinga, ...'),
    long_description=readme + '\n\n' + history,
    author="Alexandre Chaussier",
    author_email='alexandre.chaussier@temelio.com',
    url='https://github.com/Temelio/monitoring-plugins-python',
    packages=find_packages(),
    package_dir={'monitoring_plugins':
                 'monitoring_plugins'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='monitoring_plugins',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
